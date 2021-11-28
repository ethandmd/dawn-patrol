import copy

class GameItem:

    def __init__(self, name, desc, loc):
        self.name = name
        self.desc = desc
        self.loc = loc

    def __str__(self):
        msg = f"Name: {self.name}\nDescription: {self.desc}"

        return msg

    def save(self):
        '''Method for saving game items.'''
        
        return {self.name : {'desc': self.desc, 'loc':self.loc.name}}

    def copy(self):
        '''Return deepcopy of instance.'''
        return copy.deepcopy(self)

    def setLocation(self, newLoc):
        '''Change game item's location.'''
        if newLoc is self.loc:
            return False
        else:
            self.loc = newLoc

class Inventory:

    def __init__(self, items):
        self.items = items
        self.wt = sum([i.wt for i in items])
        self.cube = sum([i.cube for i in items])

    def __str__(self):
        reps = []
        #Generate name, qt for each unique item name
        for i in set([i.name for i in self.items]):
            reps.append(self.checkQt(i))
        msg = ''
        for e in reps:
            msg =+ f"\n{e[0]: (e[1]}x"

        return msg

    def checkQt(self, itemName):
        '''
        Input: item name : str
        Iterate through items and count quantities by item name.
        Return (item, qt)
        '''
        qt = 0
        for i in self.items:
            if i.name == itemName:
                qt += 1
        return name, qt

    def addItem(self,item):
        self.items.append(item)
        self.wt += item.wt
        self.cube += item.cube

    def removeItem(self, itemName):
        #Find first occurance of item name to delete
        j = [i.name for i in self.items].index(itemName)

        self.wt -= self.items[j].wt
        self.cube -= self.items[j].cube

        del self.items[j]
