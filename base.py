import sqlite3

class World:
    
    def __init__(self, name):
        self.name = name
        self.places = []
        self.placeNames = []
        self.edges = []
        self.players = []
        self.playerNames = []

    def addEdge(self, edge: tuple):
        if edge not in self.edges:
            self.edges.append(edge)

    def addPlace(self, place):
        if place not in self.places:
            self.places.append(place)
            self.placeNames.append(place.name.lower())
            return True
        else:
            return False

    def getPlace(self, name):
        try:
            idx = self.placeNames.index(name.lower())
            return self.places[idx]
        
        except ValueError as e:
            return False

    def addPlayer(self, player):
        if player not in self.players:
            self.players.append(player)
            self.playerNames.append(player.name.lower())
            return True
        else:
            return False

    def getPlayer(self, name):
        try:
            idx = self.playerNames.index(name.lower())
            return self.players[idx]

        except ValueError as e:
            return False

    def showPlayers(self):
        for p in self.playerNames:
            print(p, end=", ")

class GameItem:

    def __init__(self, name, desc, loc, maxWt, maxCb):
        self.name = name
        self.desc = desc
        self.loc = loc
        self.inventory = Inventory([], maxWt, maxCb)

    def __str__(self):
        msg = f"Name: {self.name}\nDescription: {self.desc}\nLocation: {self.loc.name}"
        msg += self.inventory.__str__()

        return msg

    def setLocation(self, loc):
        if self.loc is loc:
            pass
        else:
            self.loc = loc

    def addItem(self, item):
        self.inventory.addItem(item)
        if item.loc is self:
            pass
        else:
            item.loc.removeItem(item)
            item.setLocation(self)

    def removeItem(self, item):
        self.inventory.removeItem(item)
        item.setLocation(self.loc)

    def checkItems(self):
        '''For testing purposes only.'''
        print(self.inventory.items)

class Inventory:

    def __init__(self, items, maxWt, maxCb):
        self.items = items
        self.names = []
        self.maxWt = maxWt
        self.maxCb = maxCb
        self.wt = sum([i.wt for i in items])
        self.cb = sum([i.cb for i in items])

    def __str__(self):
        if len(self.items) == 0:
            return ''
        else:
            msg = '\nInventory:'
            for name in set([i.name for i in self.items]):
                qt = self.checkQt(name)
                msg += f"\n\t{qt[0]}: {qt[1]}x"
            msg += "\n"
        return msg

    def __contains__(self, idee):
        if idee in self.items:
            return True
        elif idee in self.names:
            return True
        else:
            return False

    def getItem(self, itemName):
        idx = self.names.index(itemName.lower())
        return self.items[idx]

    def checkQt(self, itemName): 
        qt = 0
        for item in self.items:
            if item.name == itemName:
                qt += 1
        return itemName, qt

    def addItem(self, item):
        if item.wt + self.wt <= self.maxWt:
            if item.cb + self.cb <= self.maxCb:
                self.items.append(item)
                self.names.append(item.name.lower())
                self.wt += item.wt
                self.cb += item.cb
                return True
        else:
            return

    def removeItem(self, item):
        if item in self.items:

            self.wt -= item.wt
            self.cb -= item.cb

            self.items.remove(item)

            return True

        else:
            return False

'''
class SQLWriter:
    # SQL SYNTAX TO CREATE TABLES
    cPlaces = """CREATE TABLE IF NOT EXISTS places (
                    name PRIMARY KEY,
                    desc text,
                    loc text NOT NULL,
                    edges text,
                    items text,
                    players text
                );"""

    def connect(self, filename): 

        try:
            conn = sqlite3.connect(filename)
            return conn
        except sqlite3.ProgrammingError as e:
            print(e)
            return
'''
