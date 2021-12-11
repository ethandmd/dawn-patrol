class Player:
    '''Class to store player methods.'''

    def playerFromNode(self, node):
        '''Take BSTNode data and create a player to interact with.'''
        name = node.key
        loc = node.meta['loc']
        health = node.meta['health']
        stamina = node.meta['stamina']
        wt = node.meta['wt']
        cb = node.meta['cb']
        maxWt = node.meta['maxWt']
        maxCb = node.meta['maxCb']
        inv = node.cargo
        return name, loc, health, stamina, wt, cb, maxWt, maxCb, inv

    def nodeFromPlayer(self, name, loc, health, stamina, wt, cb, maxWt, maxCb, inv):
        key = name
        meta = {'loc':loc.name,'health':health,'stamina':stamina, 'wt':wt, 'cb':cb, 'maxWt':maxWt, 'maxCb':maxCb}
        cargo = inv
        return key, meta, cargo

    def injure(self, health, amt):
        '''Reduce player health by amt. Lower bound of zero.'''
        if health - amt <= 0:
            health = 0
        else:
            health -= amt
        return health

    def exert(self,stamina, amt):
        '''Reduce player stamina by amt. Lower bound of zero.'''
        if stamina - amt <= 0:
            stamina = 0
        else:
            stamina -= amt
        return stamina

    def pickup(self, wt, cb, maxWt, maxCb, inv, item):
        if wt + item.meta['wt'] <= maxWt:
            if cb + item.meta['cb'] <= maxCb :
                wt += item.meta['wt']
                cb += item.meta['cb']
                inv.setValue(item.key, item.meta, item.cargo)
                return True
        else:
            return False
    
    def drop(self, wt, cb, inv, item):
        #Adjust cube and weight
        if wt - item.meta['wt'] <= 0:
            wt = 0
        else:
            wt -= item.meta['wt']
        if cb - item.meta['cb'] <= 0:
            cb = 0
        else:
            cb -= item.meta['cb']

        inv.removeValue(item.key) #remove item from inv
            
    def putItem(self, loc, inv, item, recipient):
        '''Put an item from inv into place.inv.'''

        #Check that item is in player inv
        if item.key in inv:
            #Check that recipient is in same location as player
            if recipient.key in loc.items:
                #Check that recipient is an item that can contain other items
                if recipient.cargo is not None:
                    #Limit item's cargo carrying capacity
                    if item.wt + recipient.meta['wt'] <= recipient.meta['Wt']+recipient.meta['cb']:
                        recipient.cargo.setValue(item.key, item.meta, item.cargo) #Add item to recipient inv
                        return True
        else:
            return False

    def asString(self, name, loc, health, stamina, inv):
        msg = "Name: " + name
        msg += "\nLocation: " + loc.name
        msg += "\nHealth: " + str(health)
        msg += "\nStamina: " + str(stamina)
        msg += "\nInventory: " + str(inv)

        return msg
