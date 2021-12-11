import os
import json
from base import BSTBuilder, Vertex, Inventory
from player import Player
from item import Item
from datetime import datetime

class Config:
    ckptFP = './ckpts/'
    vanillaFP = './ckpts/game.json'

    def __init__(self):
        #Create ckpts dir if not already there
        if not os.path.exists(self.ckptFP):
            os.mkdir(self.ckptFP)

        self.places = []
        self.commands = {
                'help' : ' (Display game help menu)',
                'pickup [item name]': ' (Pickup an item)',
                'drop [item name]' : ' (Drop an item)',
                'put [item name] [receiving name]' : ' (Put an item into another item)',
                'move [location name]' : ' (Move to a location)',
                'order [player name] [command] [command]' : ' (Have an NPC perform {command} with {command}. Yes you can have an NPC order another NPC to order another NPC ...)',
                'status' : ' (Display player status)'
                }

    def addItemToPlace(self, item, place):
        key, meta, cargo = item.asNode()
        place.items.setValue(key, meta, cargo)

    def addNPCToPlace(self, npc, place):
        key, meta, cargo = npc.asNode()
        place.npcs.setValue(key, meta, cargo)

    def addPlace(self, place):
        if place not in self.places:
            self.places.append(place)

    def displayHelp(self):
        print("Commands: ")
        for k in self.commands:
            print(k, self.commands[k])

    def createCkpt(self):
        data = {}
        for place in self.places:
            data.update(place.save())

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

    def loadGame(self, flavor):
        if flavor == 'vanilla':
            fp = self.vanillaFP
        else:
            #Get most recent ckpt
            fp = self.ckptFP + sorted(os.listdir(self.ckptFP))[-1] #.remove('game.json')

        #Load BSTBuilder
        B = BSTBuilder()
        data = self.loadCkptData(fp)
        #Sort ckpt data by place
        for place in data:
            print("Building ",place, "...")
            #Create place
            rawPlayers = data[place]['players']
            players = B.build(rawPlayers)
            rawNPCs = data[place]['npcs']
            npcs = B.build(rawNPCs)
            rawItems = data[place]['items']
            items = B.build(rawItems)
            create = Vertex(self, place, players, npcs, items)
            #Connect rooms as appropriate
            for out in data[place]['outs']:
                create.drawEdge(out)

            #Find player
            if players.root is not None:
                USER = players.root

        return USER

    def createGame(self):
        #Create places
        pass







