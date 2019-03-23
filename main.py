# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 16:41:45 2019

main.py

CLI for CoNxNect

@author: Ben
"""
import os
import cmdCLI

'''
LS list command 
'''
class cmdLS_Modules(cmdCLI.cmd):
    def do(args):
        filenames=os.listdir("AI_Players")
        #restrict to only py files, and strip .py
        for f in filenames:
            if (len(f)>3 and f[-3:]==".py"):
                print(f[:-3])
    def setHelp(self):
        self._shortHelpText="Player modules available."

'''
************************************************************
CLI command handlers
************************************************************
'''
#quit
class cmdExit(cmdCLI.cmd):
    def do(args):
        return False
    def setHelp(self):
        self._shortHelpText= "Exit Command Line Interface (CLI)."
#List something
class cmdLS(cmdCLI.cmd):
    handlers={"pmod":cmdLS_Modules}
    def do(args):
        #pmod - list installed player modules        
        if len(args)>0:
            if args[0] in cmdLS.handlers:
                cmdLS.handlers[args[0]](args[1:])
        return True
    def setHelp(self):
        self._shortHelpText= "Args: TYPE. Print list of items of given TYPE."
        self._longHelpText= "Args: TYPE. Print list of items of given TYPE.\n\nTYPE:\n--------------"
        for h in sorted(cmdLS.handlers.keys()):
            c=cmdLS.handlers[h]()
            self._longHelpText+="\n"+h +" - "+c.shortHelp()

#print help
class cmdHelp(cmdCLI.cmd):
    def do(args):
        #generic help - list all handlers and short text
        if len(args)==0 or (args[0] not in ParseCMD_handlers):
            for h in sorted(ParseCMD_handlers.keys()):
                c=ParseCMD_handlers[h]()
                print(h +" - "+c.shortHelp())
        else:
            c=ParseCMD_handlers[args[0]]()
            print("**************\n"+args[0] +"\n**************\n"+c.longHelp())
        return True
    def setHelp(self):
        self._shortHelpText= "Args: [CMD]. Print list of commands, or longer help for specified CMD."

'''
************************************************************
Main CLI cmd parser
************************************************************
return False to terminate main loop
'''
ParseCMD_handlers={"quit":cmdExit, "ls":cmdLS, "help":cmdHelp}#define handlers
def ParseCMD(cmd): 
    
    toks=cmd.split()
    if len(toks)==0: return True#basic checks
    
    if toks[0] in ParseCMD_handlers:
        return ParseCMD_handlers[toks[0]].do(toks[1:])        
    else: 
        print("Unrecognized command! Type \"help\" for command list.")
        return True
    
    
'''
Main CLI loop
'''
while(True):
    cmd=input(">")
    if not ParseCMD(cmd): break