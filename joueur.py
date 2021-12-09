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

    def move(self, door):
        exAmt = self.inventory.wt * 0.1 + 2 #Exertion amount as a function of weight
        loc = self.loc.getLoc(door)
        self.setLocation(loc)
        self.loc.addPlayer(self)
        self.exert(exAmt)

    def takeItem(self,itemName):
        try:
            item = self.loc.inventory.getItem(itemName.lower())
            success = GameItem.addItem(self, item)
            if success:
                return True

        except ValueError as e:
            print("Unable to find item.")
            return False

    def dropItem(self, itemName):
        try:
            item = self.inventory.getItem(itemName.lower())
            GameItem.removeItem(self, item)
            self.loc.addItem(item)
            return True
        except ValueError as e:
            print("Unable to find item.")
            return False

    def putItem(self, where, itemName):
        where = self.loc.inventory.getItem(where.lower())
        item = self.inventory.getItem(itemName.lower())
        if where in self.loc.inventory:
            where.addItem(item)
            return True
        else:
            return False
