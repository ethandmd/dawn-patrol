class Player:

    def __init__(self, name, loc, health, stamina, inv):
        '''inv : BSTree'''
        self.name = name
        self.loc = loc
        self.health = health
        self.stamina = stamina
        self.inv = inv

    def injure(self, amt):
        '''Reduce player health by amt. Lower bound of zero.'''
        if self.health - amt <= 0:
            self.health = 0
        else:
            self.health -= amt

    def exert(self, amt):
        '''Reduce player stamina by amt. Lower bound of zero.'''
        if self.stamina - amt <= 0:
            self.stamina = 0
        else:
            self.stamina -= amt

    def asNode(self):
        '''Method for distilling player info as BSTnode.'''
        key = self.name
        meta = {'loc':self.loc.name, 'health':self.health, 'stamina':self.stamina}
        cargo = self.inv

        return key, meta, cargo

    def move(self, newLoc):
        '''Method for moving from one location to another.'''
        #Check if locations are connected
        if self.loc.isEdge(newLoc):
            self.loc.players.removeValue(self.name) #Remove player from current loc
            self.loc = newLoc #Update location
            exAmt = self.inv.wt * 0.1 + 2 #Exertion amount
            self.exert(exAmt) #Exert player
            self.loc.players.setValue(self.asNode()) #Add player to location
            return True
        else:
            return False
            

    def takeItem(self, item):
        '''Method for taking an item from loc and adding to inv.'''
        #Check that item exists in current location
        if item.name in self.loc.items:
            #Check that player can pickup item
            if self.inv.pickup(item): #Add item to player inv
                self.loc.items.removeValue(item.name) #Remove item from loc inv
                return True
        else:
            return False

    def dropItem(self, item):
        '''Method for removing an item from inv and adding it to loc.'''
        #Check that player has item in inv
        if itemName in self.inv:
            self.inv.drop(item) #Remove item from player inv
            #Set item node data
            key, meta, cargo = item.asNode()
            self.loc.items.setValue(key, meta, cargo) #Add item to loc inv
            return True
        else:
            return False


    def putItem(self, item, recipient):
        '''Put an item from inv into place.inv.'''
        #Check that item is in player inv
        if item.name in self.inv:
            #Check that recipient is in same location as player
            if recipient.name in self.loc.items:
                #Check that recipient is an item that can contain other items
                if recipient.inv is not None:
                    self.inv.drop(item) #Remove item from inv
                    recipient.inv.pickup(item) #Add item to place inv
                    return True
        else:
            return False

    def __str__(self):
        msg = "Name: " + self.name
        msg += "\nLocation: " + self.loc.name
        msg += "\nHealth: " + str(self.health)
        msg += "\nStamina: " + str(self.stamina)
        msg += "\nInventory: " + str(self.inv)

        return msg
