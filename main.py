# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 16:41:45 2019

main.py

CLI for CoNxNect

@author: Ben
"""
#import os
import pkgutil
import importlib

import cmdCLI
import game

import PlayerModules

class G:#globals
    spec=game.gameSpec()    
    search_depth=5 #AI difficulty restriction
    
    
    def importFactories():
        ret={}
        for mod in pkgutil.iter_modules(PlayerModules.__path__):
            try:
                factoryMod=importlib.import_module("PlayerModules."+mod.name+".factory")
                ret[mod.name]=factoryMod.factory()
            except:
                print("Player module "+ mod.name+" could not be loaded!")
        return ret    
    #a dictionary of player modules by module name
    factories=importFactories()
'''
LS list command 
'''
class cmdLS_Modules(cmdCLI.cmd):
    def do(args):
        try:
            for k in G.factories:
                print(k)
        except:
            print("An error occurred enumerating packages!")
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
                cmdLS.handlers[args[0]].do(args[1:])
        return True
    def setHelp(self):
        self._shortHelpText= "Args: TYPE. Print list of items of given TYPE."
        self._longHelpText= "Args: TYPE. Print list of items of given TYPE.\n\nTYPE:\n--------------"
        for h in sorted(cmdLS.handlers.keys()):
            c=cmdLS.handlers[h]()
            self._longHelpText+="\n"+h +" - "+c.shortHelp()
#game spec
class cmdSpec(cmdCLI.cmd):
    def do(args):
        spec=game.gameSpec()
        
        try:
            spec.cols=int(input("Columns: "))
            spec.rows=int(input("Rows: "))
            spec.playerCount=int(input("Number of players: "))
            spec.victoryN=int(input("Winning run length: "))
        except:
            return True
        G.spec=spec
        
        return True
    def setHelp(self):
        self._shortHelpText= "Set game spec (grid size, player count etc.)"

#AI settings 
class cmdAIConfig(cmdCLI.cmd):
    def do(args):     
        try:
            G.search_depth=int(input("AI search depth hint: "))
        except:
            return True        
        return True
    def setHelp(self):
        self._shortHelpText= "AI restrictions and difficulty settings."
        
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

#oneGame
class cmdOneGame(cmdCLI.cmd):
    def do(args):
        match=game.game_base(G.spec)
        
        #get player types
        factory_counts={k:0 for k in G.factories}#number of players each factory must generate
        player_pos=[]# entries are (factory_name, number within factory)
        for i in range(G.spec.playerCount):
            pm_name=""
            while True:#until we get valid factory or escaped
                pm_name=input("Player "+ str(i)+" type: ")
                if pm_name=="":#escape mechanism
                    return True
                elif pm_name not in G.factories:#check valid factory
                    print("Invalid player type: "+pm_name+". Please try again...")
                else:
                    break
            player_pos.append((pm_name,factory_counts[pm_name]))
            factory_counts[pm_name]+=1
        try:        
            #generate players from each factory
            players={fname:G.factories[fname].newPlayers(G.spec, G.search_depth,
                 factory_counts[fname]) for fname in factory_counts}
        except:
            print("Failed to generate players!")
            return True
        
        try:
            #add players to match
            for (ptype,n) in player_pos:
                match.addPlayer(players[ptype][n])
        except:
            print("Failed to add players to match!")
            return True
        
        try:#run match
            match.startPlay()
            match.waitStopPlay()
        except:
            print("Error occured!")
            return True
        
    def setHelp(self):
        self._shortHelpText= "Run a single game with current specification."
        
 
'''
************************************************************
Main CLI cmd parser
************************************************************
return False to terminate main loop
'''
ParseCMD_handlers={"quit":cmdExit, "ls":cmdLS, "help":cmdHelp, 
                   "spec":cmdSpec, "aicfg":cmdAIConfig,
                   "single":cmdOneGame}#define handlers
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