# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 11:38:13 2019

@author: Ben
"""
import copy

'''
*************************************************************
gameSpec

Structure specifying the rules of a game
*************************************************************
'''
class gameSpec:
    def __init__(self):
        self.rows=6
        self.cols=7
        self.playerCount=2
        self.victoryN=4 #length of a run of the same colour in a line needed to win.
        
        
'''
*************************************************************
game_base

Base class to run a single game
*************************************************************
'''
class game_base:
    #initialised with a gameSpec
    def __init__(self, spec):
        self.spec=copy.deepcopy(spec)
        
        #0 denotes empty cell, positive numbers denote player IDs
        #cols indexed left-right
        #rows indexed bottom - top
        self.grid=[]#[[0]*spec.rows for r in range(spec.cols)]
        self.colHeights=[]#[0]*spec.cols#index of next empty cell in each column
        self.fullCols=0 #columns with no mopre spaces
        
        self.players=[]
        #TODO add a thread where this game will run
        
        #TODO add spectator
        
    #add player instance. This player will take turns after all previously added 
    #players
    def addPlayer(self, player):
        self.players.append(player)
    
    '''
    Record given player playing in given row
    -raises a RuntimeException if there is an illegal move 
    return player if that player wins, 0 on a draw or -1 otherwise
    '''
    def doMove(self, player, col):
        row=self.colHeights[col]
        if row>=self.spec.rows:
            raise RuntimeError("Invalid move. Column "+ str(col)+" is full!")
        self.colHeights[col]=row+1        
        self.grid[col][row]=player
        
        #check for victory
        
        #lengths of runs
        EWlen=1
        NSlen=1
        NWSElen=1
        SWNElen=1
        
        #EW
        for x in range(1,min(self.spec.victoryN,self.spec.cols-col)):            
            if self.grid[col+x][row]==player:
                EWlen+=1
            else: break
        for x in range(1,min(self.spec.victoryN,col+1)):            
            if self.grid[col-x][row]==player:
                EWlen+=1
            else: break
        if EWlen>=self.spec.victoryN:return player  
        
        #NS
        for x in range(1,min(self.spec.victoryN,row+1)):            
            if self.grid[col][row-x]==player:
                NSlen+=1
            else: break
        if NSlen>=self.spec.victoryN:return player  
        
        #NWSE
        for x in range(1,min(self.spec.victoryN,row+1, self.spec.cols-col)):            
            if self.grid[col+x][row-x]==player:
                NWSElen+=1
            else: break
        for x in range(1,min(self.spec.victoryN,self.spec.rows-row, col+1)):            
            if self.grid[col-x][row+x]==player:
                NWSElen+=1
            else: break
        if NWSElen>=self.spec.victoryN:return player  
        
        #SWNE
        for x in range(1,min(self.spec.victoryN,self.spec.rows-row, self.spec.cols-col)):            
            if self.grid[col+x][row+x]==player:
                SWNElen+=1
            else: break
        for x in range(1,min(self.spec.victoryN,row+1, col+1)):            
            if self.grid[col-x][row-x]==player:
                SWNElen+=1
            else: break
        if SWNElen>=self.spec.victoryN:return player  
        
        if self.colHeights[col]==self.spec.rows:#check for draw (all cols full)
            self.fullCols+=1
            if self.fullCols>=self.spec.cols:
                return 0 #draw code
        
        return -1 # no winner yet
    
    '''
    play: May throw StandardError if not enough players have been added,
    for example.
    
    Begin game loop (TODO: make it start in new thread)
    '''    
    def startPlay(self):
        if len(self.players) < self.spec.playerCount:
            raise RuntimeError("Game for "+str(self.spec.playerCount)+
                               " cannot be played with " + str(len(self.players))+" players!")
        
        self._main_loop()#TODO: run this in new thread!
    
    '''
    main game loop. TODO: make this run in new thread!
    '''
    def _main_loop(self):
        #initialise resources
        self.grid=[[0]*self.spec.rows for r in range(self.spec.cols)]
        self.colHeights=[0]*self.spec.cols#index of next empty cell in each column
        self.fullCols=0 #columns with no mopre spaces
        
        #initiate player ai threads etc
        for i in range(self.spec.playerCount):
            self.players[i].beginGame(i+1)
            
        winner =-1 #early termination default winner code
        
        while(True):
            for i in range(self.spec.playerCount):
                col=self.players[i].makeMove()
                for j in range(self.spec.playerCount):
                    if j!=i:
                        self.players[j].notifyMove(i+1,col)
                winner=self.doMove(i+1,col)#i, 0 or -1
                if winner>=0: break #win or draw
               
                
        
        #initiate player ai threads etc
        for i in range(self.spec.playerCount):
            self.players[i].endGame(winner)
            
        
    
    '''
    forceStopPlay : force game thread to quit ASAP (TODO)
    '''    
    def forceStopPlay(self):
        return
    
    '''
    waitStopPlay : join game thread (wait for it to complete) (TODO)
    ''' 
    def waitStopPlay(self):
        return