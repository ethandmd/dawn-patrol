from player import Player
from item import Item
from config import Config

class Controller:
    '''Provide game controls for a game player.'''

    def __init__(self, config):
        self.config = config

    def definePlayer(self, loc, health, stamina, inv):
        #Set up game character for user
        
        name = input("Enter your player name: ").lower()
        self.player =  Player(name, loc, health, stamina, inv) #Define Player obj
        key, meta, cargo = self.player.asNode()
        loc.players.setValue(key, meta, cargo) #Add player obj to loc
    
    def convertToVertex(self, name):
        for place in self.config.places:
            if name == place.name:
                return place

    def itemFromNode(self, node):
        '''Take BSTNode data and create an Item to interact with.'''
        name = node.key
        wt = node.meta['wt']
        cb = node.meta['cb']
        inv = node.cargo
        return Item(name, wt, cb, inv)

    def playerFromNode(self, node):
        '''Take BSTNode data and create a player to interact with.'''
        name = node.key
        loc = self.convertToVertex(node.meta['loc'])
        health = node.meta['health']
        weight = node.meta['weight']
        inv = node.cargo
        return Player(name, health, weight, inv)

    def parser(self, player, arg):
        #Check that player is a Player instance
        if not isinstance(player, Player):
            return False
        cmd = arg.lower().split() #Split cmd by whitespace
        
        if len(cmd) > 1:
            prep = cmd[0]
            exqt = cmd[1:]
        else:
            return False

        #Cases:
        ##help
        if prep == 'help':
            self.config.displayHelp()
            input("\nPress ENTER to continue...")
            return True

        ##pickup
        if prep == 'pickup':
            exqt = ' '.join(exqt)
            #Find out if an item called exqt exists
            rawItem = self.getItem(exqt)
            if rawItem is not None:
                item = self.itemFromNode(rawItem)
                return player.takeItem(item)
        
        ##drop
        if prep == 'drop':
            exqt = ' '.join(exqt)
            #Find out if an item called exqt exists
            rawItem = player.inv.getValue(exqt)
            if rawItem is not None:
                item = self.itemFromNode(rawItem)
                return player.dropItem(item) 

        ##put
        if prep == 'put':
            #Check  exqt1 & exqt2
            try:
                #Get raw item and recipient
                rawItem, rawRecipient = player.inv.getValue(exqt[0]), player.loc.items.getValue(exqt[1])
                item, recipient = self.itemFromNode(rawItem), self.itemFromNode(rawRecipient)
                #Put item
                return player.putItem(item, recipient)

            except TypeError as e:
                print(e)
                return False

        ##move
        if prep == 'move':
            exqt = ' '.join(exqt)
            #Get new loc
            newLoc = getattr(player.loc, exqt)
            if newLoc is not None:
                return player.move(newLoc)

        ##order
        if prep == 'order':
            try:
                #Find player
                rawPlayer = player.loc.npcs.getValue(exqt[0])
                if rawPlayer is not None:
                    player = self.playerFromNode(rawPlayer)
                    newCmd = ' '.join(exqt[1:])
                    return self.parser(player, newCmd)
                else:
                    return False
            except TypeError as e:
                print(e)
                return False

        ##status
        if prep == 'status':
            print(player)
            input("\nPress ENTER to continue...")
            return True
