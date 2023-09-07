# -*- coding: utf-8 -*-
'''
Created on Jul 13, 2021
@author: Claudio Ronchetti
'''
from aiida.orm import load_node
    

class AiiDATA:
    def __init__(self, node):
        self.node = node
        self.set_pk()
        
    def get_pk(self):
        return self.node.pk
        
    def set_pk(self):
        self.pk=self.node.pk
        
    def post(self):
        return {'field':'no-data'}
    
class BoolStruct(AiiDATA):
    def post(self):
        return {'value': self.node.value}
    
class CalcJobNodeStruct(AiiDATA):
    def post(self):
        from calcfunctions.adapter.factory import AiiDAFactory
        fact = AiiDAFactory()
            
        self.inputs = {i: fact.struct(self.node.inputs[i]) for i in self.node.inputs}
        self.outputs = {o: fact.struct(self.node.outputs[o]) for o in self.node.outputs}
        
        post = {
            'inputs' : {i: self.inputs[i].post() for i in self.inputs if i not in ['code']},
            'outputs' : {o: self.outputs[o].post() for o in self.outputs if o not in ['retrieved']},
            'metadata':{
                'options': self.node.get_options(),
                'aiida_references': {
                    'calcjob': self.pk,
                    'inputs': {i: self.inputs[i].get_pk() for i in self.inputs},
                    'outputs': {o: self.outputs[o].get_pk() for o in self.outputs}
                },
                'type': 'quantumespresso.pw',
                'description': 'sodium cathodes',
                'remote_workdir': self.node.get_remote_workdir(),
                'retrieve_list': self.node.get_retrieve_list(),
                'scheduler_info': {
                    'job_id': self.node.get_job_id(),
                    'detailed_job_info': self.node.get_detailed_job_info(),
                    'scheduler_state': str(self.node.get_scheduler_state()),
                    'scheduler_last_checktime': str(self.node.get_scheduler_lastchecktime())
                }
            }
        }
        try: 
            post['metadata']['stdout'] = self.node.get_scheduler_stdout()
        except Exception as e:
            post['metadata']['stdout'] = "Found exception: "+str(e)
        try: 
            post['metadata']['stderr'] = self.node.get_scheduler_stderr()
        except Exception as e:
            post['metadata']['stderr'] = "Found exception: "+str(e)
        
        
        return post
    
class DictStruct(AiiDATA):
    def post(self):
        return self.node.get_dict()
    
    
class TrajectoryDataStruct(AiiDATA):
    def post(self):
        return {
            'cif_file': self.node.get_cif(index=0).get_content(), 
            'positions': self.node.get_positions().tolist()
        }
    
class BandsDataStruct(AiiDATA):
    def post(self):
        post = [x.tolist() for x in self.node.get_bands(also_occupations=True, also_labels=False)]
        return post

class RemoteDataStruct(AiiDATA):
    def post(self):
        post = {}
        try: 
            post['remote_path'] = self.node.get_remote_path()
        except Exception as e:
             post['remote_path'] = "Found exception: " + str(e)
        try:
            post['listdir'] = self.node.listdir()
        except Exception as e:
             post['listdir'] = "Found exception: " + str(e)
        return post
       
class FolderDataStruct(AiiDATA):
    def post(self):
        return None
    
class AttributeDictStruct(AiiDATA):
    # PSEUDOPOTENTIALS
    def get_pk(self):
        return [self.node[x].pk for x in self.node]
    def set_pk(self):
        self.pk=None
    def post(self):
        return {x: {'upf_file': self.node[x].filename, 'atomic_mass': None} for x in self.node}
    
class CodeStruct(AiiDATA):
    def post(self):
        return None
    
class KpointsDataStruct(AiiDATA):
    def post(self):
        return {
            'value': self.node.get_kpoints_mesh()[0],
            'offset': self.node.get_kpoints_mesh()[1]
        }    
    
class StructureDataStruct(AiiDATA):
    def post(self):
        ase = self.node.get_ase()
        return {
            'CELL_PARAMETERS': self.node.cell,
            'POSITIONS': ase.get_positions().tolist(),
            'SYMBOLS': ase.get_chemical_symbols(),
            'formula': str(ase.symbols),
            'cif_file': str(self.node.get_cif().get_content())
        }
    
class IntStruct(AiiDATA):
    def post(self):
        return self.node.value
