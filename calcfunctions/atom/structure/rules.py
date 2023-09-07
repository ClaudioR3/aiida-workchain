# -*- coding: utf-8 -*-
'''
Created on Nov 05, 2021
@author: Claudio Ronchetti
'''
import random

def sodium_removing(molecule, **kargs):
    molecule = molecule.copy()
    # random config generator
    naidx = [x.index for x in molecule if x.symbol=='Na']
    max_removed = len(naidx)
    # RRN - removed random number is a random number between 0 (min) and max removed number
    rrn = random.randint(0, max_removed)
    # remove element for RRN times
    for j,i in enumerate(range(rrn)):
        naidx = [x.index for x in molecule if x.symbol=='Na']
        chosen = random.choice(naidx)
        # remove element at the chosen position
        # pop element in ASE atoms
        molecule.pop(chosen)
    return molecule

def manganese_replacement(molecule, **kargs):
    molecule = molecule.copy()
    # Index of manganese atoms
    Mn_idx = [x.index for x in molecule if x.symbol=='Mn']
    # define tansaction metal
    if 'transiction_metals' in kargs:
        tm = kargs['transiction_metals']
    else:
        tm = ['Ni', 'Ti']
    # define replacement step
    if 'manganese_replacement_step' in kargs:
        step = kargs['manganese_replacement_step']
    else:
        step = 2
    # define min number of manganese atoms in the system
    if 'manganese_min_number' in kargs:
        step = kargs['manganese_min_number']
    else:
        min_number = int(len(Mn_idx)/2)
    # 'replacements' is dict and it counts the global replacement
    # of manganese atoms for each transaction metals
    replacements = {}
    # 'remained' is int and it counts 
    # how many replacements remain
    remained = (len(Mn_idx) - min_number)//step
    print(min_number, remained)
    # define replacements for each transaction metals
    random.shuffle(tm)
    for elem in tm:
        replacements[elem] = random.choice(range(0, remained+1))
        remained -= replacements[elem]
    # replace manganese atoms with transaction metals
    for elem in tm:
        n_replace = replacements[elem] * step
        for i in range(n_replace):
            idx = [x.index for x in molecule if x.symbol=='Mn']
            chosen = random.choice(idx)
            # replace element at the chosen position
            molecule[chosen].symbol=elem
    # create ASE Atoms
    return molecule
            
def default_rule(molecule, **kargs):
    # create ASE Atoms
    return molecule.copy()

def all_sodium_removing(molecule, **kargs):
    molecule = molecule.copy()
    # identify the indices of Na atoms to remove
    to_remove = []
    for i,y in enumerate(molecule):
        if y.symbol=='Na': to_remove.append(y.index)
    # delete the Na atoms in the molecule
    for z in sorted(to_remove, reverse=True):
        molecule.pop(z)
    return molecule
    