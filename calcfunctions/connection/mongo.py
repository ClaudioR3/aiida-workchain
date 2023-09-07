# -*- coding: utf-8 -*-
'''
Created on Nov 05, 2021
@author: Claudio Ronchetti
'''
from pymongo import MongoClient

def get_properties(properties):
    # read properties file
    with properties.open() as prop:
        l = [line.split("=") for line in prop.readlines()]
        d = {key.strip(): value.strip() for key,value in l}
    # return dict(line.strip().split("=") for line in properties.get_content().split("\n"))
    return d 
    
def get_connection(props):
    # connection
    MONGO_URI = 'mongodb://' + props['user']+ ':' + props['password'] + '@' + props['server']+ ':' + props['port'] + '/?authSource='+ props['authSource'] + '&authMechanism=' + props['authMechanism']
    return MongoClient(MONGO_URI)