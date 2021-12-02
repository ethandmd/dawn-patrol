'''Simulated physical places for in-game world.'''
from base import GameItem, Inventory

class Place(GameItem):
    
    def __init__(self, name, desc, loc, maxWt=1e6, maxCb=1e6):
        GameItem.__init__(self, name, desc, loc, maxWt, maxCb)
        loc.addPlace(self)

        self.exits = []
        self.doors = {}
        self.players = []

    def __str__(self):
        msg = GameItem.__str__(self)
        if len(self.players) > 0:
            msg += "\nPeople:"
        for p in self.players:
            msg += f"\n\t{p.name}"
        
        msg += "\nDoors:"
        for d in self.doors:
            msg += f"\n\t{d}"

        return msg

    def addPlayer(self, player):
        if player not in self.players:
            self.players.append(player)
            return True
        else:
            return False

    def removePlayer(self, player):
        if player in self.players:
            self.players.remove(player)
            return True
        else:
            return False

    def addExit(self, loc):
        self.exits.append(loc)
        self.doors[loc.name+" door"] = loc
    
    def connect(self, loc):
        self.addExit(loc)
        loc.addExit(self)

        self.loc.addEdge((self,loc))
