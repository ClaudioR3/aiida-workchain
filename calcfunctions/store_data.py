# -*- coding: utf-8 -*-
'''
Created on Nov 05, 2021
@author: Claudio Ronchetti
'''
from aiida.engine import calcfunction
from aiida.orm import Dict, Str, SinglefileData
import calcfunctions.connection as mongo

@calcfunction
def dict2mongo(post: Dict, properties: SinglefileData) -> Str:    
    # get properties from properties file
    props = mongo.get_properties(properties)
    # connection
    conn = mongo.get_connection(props)
    # save
    saved = conn[props['database']][props['collection']].insert_one(post.get_dict())
    # return ObjectId from bson.objectid
    return Str(saved.inserted_id)