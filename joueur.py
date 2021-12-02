'''Playable and non-playable characters.'''
from base import GameItem, Inventory
class Player(GameItem):
    '''
    Base class for a game character.
    '''

    def __init__(self, name, desc, loc, maxWt, maxCb, health, stamina):
        GameItem.__init__(self, name, desc, loc, maxWt, maxCb)
        loc.addPlayer(self)

        self.health = health
        self.stamina = stamina

    def __str__(self):
        msg = GameItem.__str__(self)
        msg += f"\nHealth: {self.health}, Stamina: {self.stamina}"

        return msg

    def injure(self, amount):
        if self.health - amount <= 0:
            self.health = 0
        else:
            self.health -= amount

    def exert(self, amount):
        if self.stamina - amount <= 0:
            self.stamina = 0
        else:
            self.stamina -= amount

    def rest(self, time):
        '''Time: seconds'''
        pass

    def move(self, loc):
        exAmt = self.inventory.wt * 0.1 + 2 #Exertion amount as a function of weight
        if loc in self.loc.exits:
            self.setLocation(loc)
            self.loc.addPlayer(self)
            self.exert(exAmt)
            return True
        else:
            return False

    def takeItem(self,itemName):
        try:
            item = self.inventory.getItem(itemName)
        except ValueError as e:
            return False

        if item in self.loc.inventory:
            GameItem.addItem(self, item)
            return True
        else:
            return False

    def putItem(self, where, item):
        if where in self.loc.inventory:
            where.addItem(item)
            return True
        else:
            return False
