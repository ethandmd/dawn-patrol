'''Simulated physical places for in-game world.'''

class World:
    '''Game world, all places reside within a world.'''
    places = []

class Place:
    '''
    Base class for physical places.
    Generally, a Place will have:
        -exist in a larger world
        -connections to other places (via exits)
        -items that players can interact with
        -non-playable characters that players can interact with
        -human player(s) that are in the room.
    This information is maintained using Python built-in lists.
    '''

    def __init__(self, world, name, description='', exits=[], items=[], characters=[]):
        self.world = world
        world.places.append(self) #Add place to world
        self.name = name
        self.description = description
        self.exits = [] #Entrances and exits
        #Connect place to every exit place:
        for exit in self.exits:
            self.connect(exit)
        self.items = [] #Interactive items present
        self.players = [] #Human players
    
    ###
    #Add / Remove / Inspect place:
    ###
    def addPlayer(self, player):
        if player not in self.players:
            self.players.append(player)

    def removePlayer(self, player):
        if player in self.players:
            self.players.remove(player)

    def addItem(self, item):
        if item not in self.items: #Don't add duplicates
            self.items.append(item)

    def removeItem(self, item):
        self.items.remove(item)

    def addExit(self, place):
        self.exits.append(place)
    
    def connect(self, place):
        '''Connect two places.'''
        if place is not self and place not in self.exits: #Make sure graph has no loop edges, double edges
            self.addExit(place) #Connect this place to other place
            place.addExit(self) #Connect other place to this place

    def describe(self):
        '''Return instance attribute data as a python3 list.'''
        return [self.world, self.name, self.description, self.exits, self.items, self.players]


    def update(self):
        '''Increment timestep for all persons in place.'''
        for player in players:
            player.update()

        for character in characters:
            character.update()
