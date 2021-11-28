'''Utilities for saving the game.'''
import os
import json

def logsDir():
    '''Check current directory for game checkpoints dir if none, create one.'''
    if os.path.exists('.ckpts'):
        pass
    else:
        os.mkdir('.ckpts')

def createCheckpoint(world):
    '''
    Write current game data to python dict.
    '''

    pass

def saveGame(ckpt):

    #Check for, (create) ckpt directory
    logsDir()


    
