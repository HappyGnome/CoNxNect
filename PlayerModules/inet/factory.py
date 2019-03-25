"""
Factory class for internet players using TCP 
"""
import game#from program root
import player#from player package root
import lobbyWindow
import tkinter as tk

class factory:
    '''
    TODO: keep list of connected players (that incoming connections can be
    made with).
    
    start server on connection and maintain list of connected players
    
    Allow dialog to give instructions to connect clients and to select 
    which will be used in a game (escluding those currently in another game 
    etc.)
    '''
    def newPlayer(self, spec, search_depth):
        return self.newPlayers(spec,search_depth,1)
    def newPlayers(self, spec, search_depth, n):
        #create host window
        root=tk.Tk()
        lW=lobbyWindow.lobbyWindow(root)
        lW.pack(fill=tk.BOTH,expand=tk.YES)
        root.mainloop()
    def loadDefaultConfig(self):
        pass
    def debriefPlayer(self,player):
        pass
    def saveConfig(self):
        pass