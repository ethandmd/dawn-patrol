from player import Player
from item import Item
from config import Config

class Controller:
    '''Provide game controls for a game player.'''

    def __init__(self, config, PlayerControl):
        self.config = config
        self.PC = PlayerControl()
    '''
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
        return name, wt, cb, inv
    
    def nodeFromItem(self, name, wt, cb, inv):
        '''Take item data and create a node to store.'''
        key = name
        meta = {'wt':wt, 'cb':inv}
        cargo = inv

        return key, meta, cargo
    '''

    def parser(self, player, arg):
        #Unpack player
        name, loc, health, stamina, inv = self.PC.playerFromNode(player)

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
            return

        ##pickup
        elif prep == 'pickup':
            exqt = ' '.join(exqt)
            #Find out if an item called exqt exists
            item = loc.items.getValue(exqt)
            if item is not None: 
                self.PC.takeItem(loc, inv, item)
            else:
                return False
        ##drop
        elif prep == 'drop':
            exqt = ' '.join(exqt)
            #Find out if an item called exqt exists
            item = player.inv.getValue(exqt)
            if item is not None:
                self.PC.dropItem(loc, inv, item)
            else:
                return False
        ##put
        elif prep == 'put':
            #Check  exqt1 & exqt2
            try:
                #Get raw item and recipient
                item, recipient = inv.getValue(exqt[0]), player.loc.items.getValue(exqt[1])
                #Put item
                self.PC.putItem(loc, inv, item, recipient)

            except TypeError as e:
                print(e)
                return False

        ##move
        elif prep == 'move':
            exqt = ' '.join(exqt)
            #Get new loc
            newLoc = getattr(loc, exqt)
            if newLoc is not None:
                player.move(name, loc, stamina, inv, newLoc)
            else:
                return False
        ##order
        elif prep == 'order':
            try:
                #Find player
                sub = loc.npcs.getValue(exqt[0])
                if sub is not None:
                    newCmd = ' '.join(exqt[1:])
                    self.parser(sub, newCmd)
                else:
                    return False

            except TypeError as e:
                print(e)
                return False

        ##status
        elif prep == 'status':
            print(self.PC.asString(name, loc, health, stamina, inv)
            input("\nPress ENTER to continue...")
            return
        
        else:
            return False
        
        #Final step
        #Update player in BST
        #If not returns for failures were triggered
        key, meta, cargo = self.PC.nodeFromPlayer(name, loc, health, stamina, inv)
        loc.players.setValue(key, meta, cargo)

        return True


