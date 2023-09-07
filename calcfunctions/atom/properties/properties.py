# -*- coding: utf-8 -*-
'''
Created on Jul 09, 2021
@author: Claudio Ronchetti
'''
from aiida.engine import calcfunction

def form_energy(energy, symbols):
    # define all costants 
    energy_Mn = -427.40121591 / 2
    energy_Na = -97.01237641 
    energy_O = -64.530012244 / 2
    energy_Ni = -100.37423302
    energy_Ti  =-238.9219279 / 2
    e = 13.6057
    energy_Tot = energy
    
    n_Mn = symbols.count("Mn")
    n_Na = symbols.count("Na")
    n_O = symbols.count("O")
    n_Ni = symbols.count("Ni")
    n_Ti = symbols.count("Ti")
    n_Tot = len(symbols)
    
    fe = (energy_Tot - ( n_Mn*energy_Mn + 
                                 n_Na*energy_Na + 
                                 n_O*energy_O + 
                                 n_Ni*energy_Ni + 
                                 n_Ti*energy_Ti) * e) / n_Tot
    return fe

def redox_potential(E_x2, symbols):
    # define all costants 
    e = 13.6057
    E_x1 = -1670.88539408 * e * 4
    # E_x2 = -2254.49189795 * e
    E_Na = -97.01237641 * e
    
    x2 = symbols.count("Na") / 24
    x1 = 0
    rp = - (E_x2 - E_x1 - (x2 - x1) * E_Na ) / (x2 - x1)
    return rp

@calcfunction
def add_properties(document: Dict) ->  Dict:
    doc = document.get_dict()
    energy = doc['outputs']['output_parameters']['energy']
    symbols = doc['inputs']['structure']['SYMBOLS']
    # calculate formation energy
    fe = form_energy(energy, symbols)
    # calculate redox potential
    rp = redox_potential(energy, symbols)
    # update calculation on MongoDB
    doc['outputs']['output_parameters']['formation_energy'] = fe
    doc['outputs']['output_parameters']['formation_energy_units'] = 'eV / atom'
    doc['outputs']['output_parameters']['redox_potential'] = rp
    return Dict(dict=doc)