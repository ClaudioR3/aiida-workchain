'''
Created on Jul 13, 2021
@author: Claudio Ronchetti
'''

from calcfunctions.adapter.structure import *

class AiiDAFactory:
    '''
    This class is based on Factory Method with the 'struct' reflection function.
    '''
    def __init__(self):
        pass
    
    def struct(self,node):
        '''
        The function takes the primary key of a AiiDA node and returns the relative data_structure.
        Otherwise, return 'DataStructure not found'.
        @param subscriber: list, list of Subscriber objects to set all Subscriber objetcs in subscriber attribute in 
        nameArgOperation class, and then save sys.argv in log Document.
        @return object: subclass Operation, return the subclass of Operation with name 'nameArgOperation'
        '''
        try:
            struct=type(node).__name__
            struct_name="calcfunctions.adapter.structure."+struct+"Struct"
            
            the_class = self.my_import(struct_name)
            objecT=the_class(node)
            return objecT
        except :
            #case: operation not found
            raise("Data structure (type={}) not found!".format(str(node)))
            
        
    def my_import(self,name):
        '''
        Define the class in 'name'.
        @param name: string, the path of 'name' class. For example Operazions.HelpOperation
        '''
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod