'''Playable and non-playable characters.'''

class Player:
    '''
    Base class for a game character.
    Players have:
        -name
        -description
        -health
        -stamina
        -current location
        -inventory weight limit
        -inventory cube limit
        -inventory of items
    '''

    def __init__(self, name, description, health, stamina, location, maxWt, maxCube, inventory={'wt':0,'cube':0,'items':[]}):
        self.name = name
        self.description = description
        self.health = health
        self.stamina = stamina
        self.location = location
        location.players.append(self) #Add player to location
        self.maxWt = maxWt
        self.maxCube = maxCube
        self.inventory = inventory

    def move(self, newLocation):
        if newLocation in self.location.exits:
            newLocation.addPlayer(self)
            self.location = newLocation
            
        elif newLocation is self.location:
            print("Player location unchanged.")

        else:
            print(f"{newLocation.name} not connected to {self.location.name}.")
    
    ###
    #Add / Remove items from player inventory
    ###
    def takeItem(self, item):
        '''
        Check the following conditions for taking an item:
        1. If the item is in the player's location
            2. If the player can carry the item's weight
                3a. If the item will increase the player's cube limit
                3b. If the player can carry the item's cube

        Return True if player picked up the item.
        Return False if player can not pick up the item.
        '''
        if item in self.location.items: #Check if item is present in location
            if item.weight + self.inventory['wt'] <= self.maxWt: #Check weight limit
                if item.contents: #If item can carry other items
                    self.maxCube += item.cube #Increase player's max cube
                    self.inventory['items'].append(item) #add item to inventory
                    self.inventory['wt'] += item.weight #increment inventory weight
                    item.decrementQuantity(1) #decrement item duplicity
                    item.setLocation(self)

                    return True

                else: #If item can not carry other items
                    if item.cube + self.inventory['cube'] <= self.maxCube: #Check cube limiy
                        self.inventory['cube'] += item.cube
                        self.inventory['items'].append(item) #add item to inventory
                        self.inventory['wt'] += item.weight #increment inventory weight
                        item.decrementQuantity(1) #decrement item duplicity
                        item.setLocation(self)

                        return True
        else:
            return False

    def removeItem(self, item):
        if item in self.inventory['items']:
            self.inventory['items'].remove(item)
            self.inventory['weight'] -= item.weight
            self.inventory['cube'] -= item.cube
        else:
            print("Item is not in inventory")

    ###
    #Injured / Exert player
    ###
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

    ###
    #Player Status
    ###
    def describe(self):
        '''Return instance attributes as a python3 list.'''

        return list(self.__dict__.values())

    def update(self):
        '''Increment time on player.'''
        #Regain stamina with time increment
        if self.stamina < 100:
            self.stamina += 1

        #Check if player is dead
        if self.health <= 0:
            self.location.removePlayer(self)
