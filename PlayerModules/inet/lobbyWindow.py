# -*- coding: utf-8 -*-
'''
lobbyWindow

Define a class derived from tk.Frame to allow player clients
to establish tcp link

@author Ben 
'''
import tkinter as tk

class lobbyWindow(tk.Frame):
    #players will be added to found players
    def __init__(self, root, foundPlayers):
        super.__init__(self,master=root)
        