# -*- coding: utf-8 -*-
'''
Created on Nov 05, 2021
@author: Claudio Ronchetti
'''
from aiida.engine import calcfunction
from aiida.orm import load_node, Int, Dict
from calcfunctions.adapter.factory import AiiDAFactory

@calcfunction
def calc2dict(calcjob_pk: Int) -> Dict:
    saved = False
    c = load_node(calcjob_pk.value)
    post = AiiDAFactory().struct(c).post()
    return Dict(dict=post)