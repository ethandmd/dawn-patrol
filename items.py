'''In-game items'''
from base import GameItem

class Item(GameItem):
    '''Item base class'''

    def __init__(self, name, desc, loc, wt, cube, qt, contents=False):
        GameItem.__init__(self, name, desc, loc)
        self.wt = wt
        self.cube = cube
        self.qt = qt

        if contents: #If item can carry other items
            self.contents = True
            self.items = []
            self.invWt = 0
            self.invCube = 0
        else:
            self.contents = False

    def __str__(self):
        msg = GameItem.__str__(self)

        #Add attributes unique to this class
        msg += f"\nQuantity: ({self.qt}x)"
        if self.contents:
            m = f"\nContents: {self.items}\nWeight: {self.invWt}/{self.wt}, Cube: {self.invCube}/{self.cube}"
            msg += m
        return msg

    def save(self):
        '''Method for saving item.'''
        data = GameItem.save(self)
        data[self.name]['wt'] = self.wt
        data[self.name]['cube'] = self.cube
        data[self.name]['qt'] = self.qt

        if self.contents:
            data[self.name]['contents'] = True
            data[self.name]['items'] = self.items
            data[self.name]['invWt'] = self.invWt
            data[self.name]['invCube'] = self.invCube
        else:
            data[self.name]['contents'] = False

        return data

    def setLocation(self,newLocation):
        '''Change item location.'''
        if newLocation is self.location:
            return False

        else:
            self.location = newLocation
            return True

    def addContents(self, item):
        '''If item can contain other items, add new item.'''
        if self.contents: #Ensure condition #1 is met.
            #Check that item can carry new item.
            if item.wt + self.invWt <= self.wt:
                if item.cube + self.invCube <= self.cube:
                    #Add new item
                    self.items.append(item)
                    self.invWt += item.wt
                    self.invCube += item.cube

                    return True
            
        return False

    def decrementQuantity(self, amount):
        '''Reduce item's quantity with lower bound of 0.'''
        if self.quantity - amount <= 0: #Check lower bound
            self.quantity = 0
        else:
            self.quantity -= amount

    def update(self):
        #Check if item still exists
        if self.quantity == 0:
            #If not, then remove item from game
            self.location.removeItem(self)
        else:
            pass


#Tests
chips = Item('juanitas', 'tortilla chips you love to eat.', 'LOCATION', 1,1,3,contents=False)
print(chips)
chips.__str__()
