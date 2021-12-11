class Player:
    '''Class to store player methods.'''
    def convertToVertex(self, name):
        for place in self.config.places:
            if name == place.name:
                return place

    def playerFromNode(self, node):
        '''Take BSTNode data and create a player to interact with.'''
        name = node.key
        loc = Player.convertToVertex(node.meta['loc'])
        health = node.meta['health']
        weight = node.meta['weight']
        inv = node.cargo
        return name, loc, health, weight, inv

    def nodeFromPlayer(self, name, loc, health, stamina, inv):
        key = name
        meta = {'loc':loc.name,'health':health,'stamina':stamina}
        cargo = inv
        return key, meta, cargo

    def injure(health, amt):
        '''Reduce player health by amt. Lower bound of zero.'''
        if health - amt <= 0:
            health = 0
        else:
            health -= amt
        return health

    def exert(stamina, amt):
        '''Reduce player stamina by amt. Lower bound of zero.'''
        if stamina - amt <= 0:
            stamina = 0
        else:
            stamina -= amt
        return stamina

    def move(name, loc, stamina, inv, newLoc):
        '''Method for moving from one location to another.'''

        #Check if locations are connected
        if loc.isEdge(newLoc):
            loc.players.removeValue(name) #Remove player from current loc
            exAmt = inv.wt * 0.1 + 2 #Exertion amount
            Player.exert(stamina, exAmt) #Exert player
            return True
        else:
            return False
            

    def takeItem(loc, inv, item):
        '''Method for taking an item from loc and adding to inv.'''

        #Check that item exists in current location
        if item.name in loc.items:
            #Check that player can pickup item
            if inv.pickup(item): #Add item to player inv
                loc.items.removeValue(item.name) #Remove item from loc inv
                return True
        else:
            return False

    def dropItem(loc, inv, item):
        '''Method for removing an item from inv and adding it to loc.'''
        #Check that player has item in inv
        if inv.drop(item): #Remove item from player inv
            loc.items.setValue(item.key, item.meta, item.cargo) #Add item to loc inv
            return True
        else:
            return False


    def putItem(loc, inv, item, recipient):
        '''Put an item from inv into place.inv.'''

        #Check that item is in player inv
        if item.name in inv:
            #Check that recipient is in same location as player
            if recipient.name in loc.items:
                #Check that recipient is an item that can contain other items
                if recipient.cargo is not None:
                    inv.drop(item) #Remove item from inv
                    recipient.cargo.setValue(item.key, item.meta, item.cargo) #Add item to recipient inv
                    return True
        else:
            return False

    def asString(name, loc, health, stamina, inv):
        msg = "Name: " + name
        msg += "\nLocation: " + loc.name
        msg += "\nHealth: " + str(health)
        msg += "\nStamina: " + str(stamina)
        msg += "\nInventory: " + str(inv)

        return msg
