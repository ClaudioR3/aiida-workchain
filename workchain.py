# -*- coding: utf-8 -*-
'''
Created on Jul 09, 2021
@author: Claudio Ronchetti
'''
from aiida.engine import run, launch, run_get_pk, WorkChain, while_, if_
import calcfunctions.atom as Atom
import calcfunctions.adapter as Adapter
from calcfunctions.store_data import dict2mongo
from aiida.orm import SinglefileData, Dict, KpointsData, UpfData, Code, Str, Int, Bool, load_node
from aiida.orm.nodes.data.upf import get_pseudos_from_structure
import os, json


class PwWorkChain(WorkChain):
    """
    List of pw errors:
    (None, None)
    (0, None)
    (303, 'The retrieved folder did not contain the required required XML file.')
    (305, 'Both the stdout and XML output files could not be read or parsed.')
    (312, 'The stdout output file was incomplete probably because the calculation got interrupted.')
    (340, 'The calculation stopped prematurely because it ran out of walltime but the job was killed by the scheduler before the files were safely written to disk for a potential restart.')
    (400, 'The calculation stopped prematurely because it ran out of walltime.')
    (410, 'The electronic minimization cycle did not reach self-consistency.')
    (462, 'The code failed during the cholesky factorization.')
    (501, 'Then ionic minimization cycle converged but the thresholds are exceeded in the final SCF.')
    (510, 'The electronic minimization cycle failed during an ionic minimization cycle.')
    (531, 'The electronic minimization cycle did not reach self-consistency.')
    """
    
    @classmethod
    def define(cls, spec):
        super().define(spec)
        spec.input('conn_properties', valid_type = SinglefileData)
        spec.input('calc_properties', valid_type = SinglefileData)
        spec.input('xyz_file', valid_type = SinglefileData)
        spec.input('random_generator', valid_type = Bool)
        spec.outline(
            cls.structure_generator,
            if_(cls.is_not_symmetry_equivalence)(
                cls.pw_calculation,
                while_(cls.is_timeout)(
                    cls.pw_restart
                ),
                cls.adapter,
                # cls.add_properties,
                if_(cls.is_not_crashed)(cls.store)
            )
            
            # cls.validate
        )
        spec.output('objectid', valid_type = Str)
        spec.exit_code(601, "WARNING_SYMMETRY_CHECK", message = "The new molecule is symmetry equivalence with a stored molecule.")
        spec.exit_code(602, "ERROR_CRASHED_SYSTEM", message = "An system error is occurred during PwCalculation.")
        spec.exit_code(603, "ERROR_SAVE_PWCALCULATION", message = "An error is occurred during PwCalculation storage.")

    def structure_generator(self):
        # read json file of calculation properties
        cp = json.loads(self.inputs.calc_properties.get_content())
        self.ctx.new_structure = Atom.structure_generator(
            xyz_file = self.inputs.xyz_file,
            rand = self.inputs.random_generator,
            args = Dict(dict=dict(cp))
        )
        
    def is_not_symmetry_equivalence(self):
        self.ctx.symmetry_check = Atom.symmetry_equivalence_check(
            self.ctx.new_structure,
            self.inputs.conn_properties)
        # self.ctx.symmetry_check = Bool(True)
        if self.ctx.symmetry_check.value: 
            self.exit_codes.WARNING_SYMMETRY_CHECK
        return self.ctx.symmetry_check.value == False
            

    def pw_calculation(self):
        # read json file of calculation properties
        cp = json.loads(self.inputs.calc_properties.get_content())
        # define kpoints
        kp = KpointsData()
        kp.set_kpoints_mesh(cp['kpoints']['mesh'],offset=cp['kpoints']['offset'])
        # define Hubbard_U
        elements = set([m.symbol for m in self.ctx.new_structure.get_ase()])
        to_remove = []
        if "hubbard_u" in cp["parameters"]["SYSTEM"]:
            for x in cp["parameters"]["SYSTEM"]["hubbard_u"]:
                if x not in elements: to_remove.append(x)
        for x in to_remove: cp["parameters"]["SYSTEM"]["hubbard_u"].pop(x)
        # ps = {elem: UpfData.get_or_create(
        #     os.path.abspath(path),
        #     use_first=True)[0]
        #       for elem, path in cp['pseudos'].items() if elem in elements}
        # define calculation inputs
        inputs = {
            'structure': self.ctx.new_structure,
            'kpoints': kp,
            'parameters': Dict(dict=cp['parameters']),
            'pseudos': get_pseudos_from_structure(self.ctx.new_structure, 'upf_enea_psl'),
            'metadata': cp['metadata'],
            'parallelization': Dict(dict=cp['parallelization'])
        }
        # define code
        code = Code.get_from_string(cp['codename'])
        # run calculation   
        builder = code.get_builder()   
        if 'settings' in cp: builder.settings = Dict(dict=cp['settings'])
        _ , node = launch.run.get_node(builder, **inputs)
        self.ctx.pw_node = node
        # if self.ctx.pw_calculation_exit_status==312: 
        #     self.exit_codes.ERROR_CRASHED_SYSTEM
        
    def is_timeout(self):
        """
        (400, 'The calculation stopped prematurely because it ran out of walltime.')
        """
        return self.ctx.pw_node.exit_status == 400
    
    def is_not_crashed(self):
        """
        (312, 'The stdout output file was incomplete probably because the calculation got interrupted.')
        """
        return self.ctx.pw_node.exit_status != 312
        
    def pw_restart(self):
        print("restarting!")
        # Load failed node
        failed_calculation = self.ctx.pw_node
        # Load Calculation Builder for restarting
        restart_builder = failed_calculation.get_builder_restart()
        # Set parameters for restarting
        parameters = restart_builder.parameters.get_dict()
        parameters['CONTROL']['restart_mode']='restart'
        restart_builder.parameters=Dict(dict=parameters)
        restart_builder.parent_folder=failed_calculation.outputs.remote_folder
        restart_builder.metadata.label='Restarting from PwCalculation<{}>'.format(failed_calculation.pk)
        # restart PwCalculation
        _ , node = launch.run.get_node(restart_builder)
        self.ctx.pw_node = node
        
    def adapter(self):
        self.ctx.post = Adapter.calc2dict(Int(self.ctx.pw_node.pk))
        
    def store(self):
        self.out('objectid', dict2mongo(self.ctx.post, self.inputs.conn_properties))
         
