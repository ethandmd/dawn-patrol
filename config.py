import os
import time
import json
from maps import Map
from base import BSTBuilder, Vertex
from player import Player
from score import ScoreCard
from datetime import datetime, timedelta

class Config:
    '''
    Class for generic utility functions associated with game operations.
    '''

    ckptFP = './.ckpts/'
    vanillaFP = './.ckpts/vanilla.json'
    preambleFP = '.preamble.txt'

    def __init__(self):
        #Create ckpts dir if not already there
        if not os.path.exists(self.ckptFP):
            os.mkdir(self.ckptFP)
        self.map = Map()
        self.places = []
        self.edges = []
        self.timeLeft = timedelta(seconds=300)
        self.scoreCard = ScoreCard()
        self.commands = {
                'help' : ' (Display game help menu)',
                'pickup [item name]': ' (Pickup an item)',
                'drop [item name]' : ' (Drop an item)',
                'put [item name] [receiving name]' : ' (Put an item into another item)',
                'takeout [item name] [giver name]' : ' (Take an item out of another item)',
                'move [location name]' : ' (Move to a location)',
                'order [player name] [command] {command}' : ' (Have an NPC perform {command} with {command}. An NPC order another NPC ...)',
                'status' : ' (Display player status)',
                'inspect [name]' : ' (Display object, enter "room" to inspect current room)',
                'save' : ' (Save current game data)',
                'quit' : ' (Exit current game)'
                }

    def gameChoice(self):
        '''Interactive pre-game menu.'''

        choice = None
        while choice is None:
            choice = input("Would you like to start a new game ([y]es / [n]o): ").lower()
            
            if choice == '' or choice[0] == 'y':
                return 'newGame'
            elif choice[0] == 'n':
                return 'loadGame'
            else:
                choice = None

    def getRestTime(self):
        '''Get a real valued number between 0-100.'''

        secs = None
        while secs is None:
            try:
                secs = int(input("Enter seconds to rest: "))
                if secs < 0:
                    return 0
                elif secs > 100:
                    return 100
                else:
                    return secs

            except ValueError as e:
                secs = None

    def addEdge(self, a, b):
        if (a,b) not in self.edges:
            self.edges.append((a,b))
            return True
        else:
            return False

    def updateTime(self, timeLeft):
        '''Utility function for save game feature. Ensures saved checkpoint has appropriate time left.'''
        self.timeLeft = timeLeft

    def getVertex(self, out):
        '''Retrieve a node in the 'world' graph.'''
        for place in self.places:
            if out == place.name:
                return place

    def addPlace(self, place):
        '''Have config class track a new node in the 'world' graph.'''
        if place.name not in self.places:
            self.places.append(place)
    
    def clear(self):
        '''Clear console screen.'''
        os.system('cls' if os.name == 'nt' else 'clear')

    def displayHelp(self):
        '''Display game commands and options.'''
        print("Commands: ")
        for k in self.commands:
            print(k, self.commands[k])
        print("Map:")
        print(self.map)

    def createCkpt(self):
        '''Store current game data as a python dict.'''
        data = {'config':{'edges':self.edges, 'timeLeft':self.timeLeft.seconds}, 'places':{}}
        for place in self.places:
            data['places'].update(place.save())

        return {'ckpt':data}

    def save(self):
        '''Save game data to json file.'''
        ckpt = self.createCkpt() #Create game ckpt
        s = str(datetime.now()).split('.')[0]
        t = '_'.join(s.split())
        filename = self.ckptFP + t + '.json' #ckpt file name
        try:
            with open(filename, 'w') as f:
                json.dump(ckpt, f, indent=4)
            
            return True

        except TypeError as e:
            print(e)
            return False

    def loadCkptData(self, fp):
        '''Read data from json file.'''
        #load ckpt
        with open(fp, 'r') as f:
            ckpt = json.load(f)

        return ckpt['ckpt']

    def loadGame(self, flavor=None):
        '''Load json data and read values into a game.'''

        if flavor == 'vanilla':
            fp = self.vanillaFP
        else:
            try:
                #Get most recent ckpt
                rcntCkpt = sorted(os.listdir(self.ckptFP))[-2]
                fp = self.ckptFP + rcntCkpt
            except IndexError as e:
                print("No saved checkpoints to load!")
                print("Loading new game...")
                time.sleep(1)
                fp = self.vanillaFP

        #Load BSTBuilder
        USER = None
        B = BSTBuilder()
        data = self.loadCkptData(fp)
        #Sort ckpt data by place
        for place in data['places']:
            #Create place
            rawPlayers = data['places'][place]['players']
            players = B.build(rawPlayers)
            rawNPCs = data['places'][place]['npcs']
            npcs = B.build(rawNPCs)
            rawItems = data['places'][place]['items']
            items = B.build(rawItems)
            create = Vertex(self, place, players, npcs, items)
            
            #Find player if applicable
            if players.root is not None:
                USER = players.root

        #Connect rooms as appropriate
        for tup in data['config']['edges']:
            a,b = self.getVertex(tup[0]), self.getVertex(tup[1])
            a.drawEdge(b)

        #Update time from ckpt
        timeLeft = timedelta(seconds = data['config']['timeLeft']) 
        self.updateTime(timeLeft)

        return USER, self.timeLeft

    def createGame(self):
        '''Create starting 'vanilla' game checkpoint.'''
        pass







