import os
import json
from base import BSTBuilder, Vertex
from player import Player
from item import Item
from datetime import datetime

class Config:
    ckptFP = './.ckpts/'
    vanillaFP = './.ckpts/game.json'

    def __init__(self):
        #Create ckpts dir if not already there
        if not os.path.exists(self.ckptFP):
            os.mkdir(self.ckptFP)
        self.places = []
        self.edges = []
        self.commands = {
                'help' : ' (Display game help menu)',
                'pickup [item name]': ' (Pickup an item)',
                'drop [item name]' : ' (Drop an item)',
                'put [item name] [receiving name]' : ' (Put an item into another item)',
                'move [location name]' : ' (Move to a location)',
                'order [player name] [command] [command]' : ' (Have an NPC perform {command} with {command}. An NPC order another NPC ...)',
                'status' : ' (Display player status)',
                'inspect [name]' : ' (Display object in question)',
                'save' : ' (Save current game data)',
                'quit' : ' (Exit current game)'
                }

    def addEdge(self, a, b):
        if (a,b) not in self.edges:
            self.edges.append((a,b))
            return True
        else:
            return False

    def getVertex(self, out):
        for place in self.places:
            if out == place.name:
                return place

    def addPlace(self, place):
        if place.name not in self.places:
            self.places.append(place)
    
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def displayHelp(self):
        print("Commands: ")
        for k in self.commands:
            print(k, self.commands[k])

    def createCkpt(self):
        data = {'config':{'edges':self.edges}, 'places':{}}
        for place in self.places:
            data['places'].update(place.save())

        return {'ckpt':data}

    def save(self):
        '''Save game data to json file.'''
        ckpt = self.createCkpt() #Create game ckpt
        s = str(datetime.now()).split('.')[0]
        t = '-'.join(s.split())
        filename = self.ckptFP + t + '.json' #ckpt file name
        try:
            with open(filename, 'w') as f:
                json.dump(ckpt, f, indent=4)
            
            return True

        except TypeError as e:
            print(e)
            return False

    def loadCkptData(self, fp):
        #load ckpt
        with open(fp, 'r') as f:
            ckpt = json.load(f)

        #ckpt = ckpt['ckpt']
        #Default, use most recent ckpt
        return ckpt['ckpt']

    def loadGame(self, flavor=None):
        if flavor == 'vanilla':
            fp = self.vanillaFP
        else:
            #Get most recent ckpt
            fp = self.ckptFP + sorted(os.listdir(self.ckptFP))[-1] #.remove('game.json')

        #Load BSTBuilder
        B = BSTBuilder()
        data = self.loadCkptData(fp)
        #Sort ckpt data by place
        for place in data['places']:
            print("Building "+place+ "...")
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

        return USER

    def createGame(self):
        #Create places
        pass







