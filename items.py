'''In-game items'''

class Item:
    '''Item base class'''

    def __init__(self, name, weight, cube, description, location, quantity=1, contents = False):
        self.name = name
        self.weight = weight
        self.cube = cube
        self.description = description
        self.location = location
        location.addItem(self)
        self.quantity = quantity
        if contents:
            self.contents = {'cube':0, 'items':[]}

    def describe(self):
        '''Return instance attributes as a python3 list.'''
        #return [self.name, self.weight, self.cube, self.description, self.location, self.duplicity, self.contents]
        return list(self.__dict__.values())

    def setLocation(self,newLocation):
        '''Change item location.'''
        if newLocation is self.location:
            print("Location unchanged.")

        else:
            self.location = newLocation

    def addContents(self, item):
        if contents:
            if item.cube + self.contents['cube'] <= self.cube:
                self.contents['cube'] += item.cube
                self.contents['items'].append(item)

        else:
            print(f"Unable to fit {item} in {self.name}.")

    def decrementQuantity(self, amount):
        if self.quantity - amount <= 0:
            self.quantity = 0
        else:
            self.quantity -= amount

    def update(self):
        if self.quantity == 0:
            self.location.removeItem(self)
        else:
            pass
