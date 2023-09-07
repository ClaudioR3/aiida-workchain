# -*- coding: utf-8 -*-
'''
Created on Nov 05, 2021
@author: Claudio Ronchetti
'''
from aiida.engine import calcfunction
from aiida.orm import Int, SinglefileData, List, StructureData, Bool, Dict
from ase.io import read
import numpy as np
import calcfunctions.atom.structure.rules as Rules
import warnings

@calcfunction
def structure_generator(xyz_file: SinglefileData, rand: Bool, args: Dict) -> StructureData:
    args = args.get_dict()
    # read xyz file in ase
    with xyz_file.open() as xyz_opened:
        molecule=read(xyz_opened)
    
    if rand.value: 
        #cell = np.array(molecule.cell)
        # define rules
        if 'rules' in args:
            rules = args['rules']
        else:
            rules = ['manganese_replacement']
        # apply rules to random molecule starting by source molecule
        for rule in rules: 
            try:
                molecule = getattr(Rules, rule)(molecule, **args)
                #if rule=='manganese_replacement':
                #    molecule = Rules.manganese_replacement(molecule)
            except AttributeError as e:
                warnings.warn('Rule %s not found in calcfunctions.atom.structure.rules module! %s ' % (rule, str(e)))
    o = [x for x in molecule if x.symbol=='O']
    na = [x for x in molecule if x.symbol=='Na']
    mn = [x for x in molecule if x.symbol=='Mn']
    ni = [x for x in molecule if x.symbol=='Ni']
    ti = [x for x in molecule if x.symbol=='Ti']
    print("O: {} , Na: {} , Mn: {}, Ni: {}, Ti: {} ".format(len(o), len(na), len(mn), len(ni), len(ti)))
    # return random molecule
    return StructureData(ase=molecule)

