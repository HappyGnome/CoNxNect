# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 17:44:21 2019

@author: Ben
"""

class cmd:   
    #do command line actions    
    def do(args):
        print("TODO: add command!")
        
    def __init__(self):
        self._shortHelpText="TODO: add short help text!"
        self._longHelpText=""
        self.setHelp()#reset help strings in derived class
        
    #set help strings here in derived classes
    def setHelp(self):
        return
    def shortHelp(self):
        return self._shortHelpText
    def longHelp(self):
        
        if self._longHelpText:
            return self._longHelpText
        else: return self._shortHelpText