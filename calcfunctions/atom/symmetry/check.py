# -*- coding: utf-8 -*-
'''
Created on Jul 09, 2021
@author: Claudio Ronchetti
'''
from aiida.engine import calcfunction
from aiida.orm import StructureData, SinglefileData, Bool
from ase import Atoms
from ase.utils.structure_comparator import SymmetryEquivalenceCheck
import calcfunctions.connection as MONGO

def get_ase(**args) -> Atoms:
    a = Atoms(cell = args['CELL_PARAMETERS'], positions = args['POSITIONS'])
    a.set_chemical_symbols(args['SYMBOLS'])
    if False in a.get_pbc(): a.set_pbc([True, True, True])
    return a

@calcfunction
def symmetry_equivalence_check( structure: StructureData, properties: SinglefileData ) -> Bool:
    
    comp = SymmetryEquivalenceCheck()
    new_atoms = structure.get_ase()
    if False in new_atoms.get_pbc(): new_atoms.set_pbc([True, True, True])
    
    symmetry_check = False
    
    # get properties from properties file
    props = MONGO.get_properties(properties)
    
    # connection
    conn = MONGO.get_connection(props)
    
    query = {
        'metadata.type': 'quantumespresso.pw',
        'metadata.description': 'sodium cathodes'
    },{'inputs.structure':1}
    cursor = conn[props['database']][props['collection']].find(*query)
    
    for x in cursor:
        atoms = get_ase(**x['inputs']['structure'])
        if comp.compare(new_atoms, atoms):
            symmetry_check = True
            break
    return Bool(symmetry_check)