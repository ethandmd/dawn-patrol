import time
import sys

class Controller:
    '''Provide game controls for a game player.'''

    def __init__(self, config, PlayerControl):
        self.config = config
        self.PC = PlayerControl()
    
    def convertToVertex(self, name):
        for place in self.config.places:
            if name == place.name:
                return place
    '''
    def itemFromNode(self, node):
        Take BSTNode data and create an Item to interact with.
        name = node.key
        wt = node.meta['wt']
        cb = node.meta['cb']
        inv = node.cargo
        return name, wt, cb, inv
    
    def nodeFromItem(self, name, wt, cb, inv):
        Take item data and create a node to store.
        key = name
        meta = {'wt':wt, 'cb':inv}
        cargo = inv

        return key, meta, cargo
    '''

    def parser(self, player, arg):
        print()
        #Unpack player
        name, loc, health, stamina, wt, cb, maxWt, maxCb, inv = self.PC.playerFromNode(player)
        loc = self.convertToVertex(loc)
        
        cmd = arg.lower().split() #Split cmd by whitespace
        
        if len(cmd) >= 1:
            prep = cmd[0]
            exqt = cmd[1:]
        else:
            prep = None

        #Cases:
        ##help
        if prep == 'help':
            self.config.displayHelp()
            input("\nPress ENTER to continue...")

        ##pickup
        elif prep == 'pickup':
            exqt = ' '.join(exqt)
            #Find out if an item called exqt exists
            item = loc.items.getValue(exqt)
            if item is not None: 
                if self.PC.pickup(wt, cb, maxWt, maxCb, inv, item):
                    loc.items.removeValue(item.key)
                    print("Successfully picked up",exqt)
                    time.sleep(2)
            else:
                print("Unable to pickup",exqt)
                time.sleep(2)
        ##drop
        elif prep == 'drop':
            exqt = ' '.join(exqt)
            #Find out if an item called exqt exists
            item = inv.getValue(exqt)
            if item is not None:
                self.PC.drop(wt, cb, inv, item)
                loc.items.setValue(item.key, item.meta, item.cargo)
                print("Successfully dropped", exqt)
                time.sleep(2)
            else:
                print("Unable to drop",exqt)
                time.sleep(2)
        ##put
        elif prep == 'put':
            #Check  exqt1 & exqt2
            try:
                #Get raw item and recipient
                item, recipient = inv.getValue(exqt[0]), loc.items.getValue(exqt[1])
                #Put item
                if self.PC.putItem(loc, inv, item, recipient):
                    self.PC.drop(wt, cb, inv, item)
                    print("Succesfully put",exqt1,"in",exqt2)
                    time.sleep(2)
            except TypeError as e:
                print(e)
                print("Unable to put",exqt1,"in",exqt2)
                time.sleep(2)

        ##move
        elif prep == 'move':
            exqt = ' '.join(exqt)
            #Get new loc
            try:
                newLoc = getattr(loc, exqt)
            except AttributeError as e:
                print(e)
                newLoc = None

            if newLoc is not None:
                loc.players.removeValue(name) #Remove player from old loc
                loc = newLoc #Update loc
                stamina = self.PC.exert(stamina, wt*0.1+2)
                print("Successfully moved to",loc.name)
                time.sleep(2)
            else:
                print("Unable to move to",exqt)
                time.sleep(2)
        ##order
        elif prep == 'order':
            try:
                #Find player
                sub = loc.npcs.getValue(exqt[0])
                if sub is not None:
                    newCmd = ' '.join(exqt[1:])
                    self.parser(sub, newCmd)
                    print("Successfully ordered",sub.key,"to",newCmd)
                    time.sleep(2)
                else:
                    print("Unable to order this person")
                    time.sleep(2)

            except TypeError as e:
                print(e)
                print("Unable to perform order")
                time.sleep(2)

        ##status
        elif prep == 'status':
            print(self.PC.asString(name, loc, health, stamina, inv))
            input("\nPress ENTER to continue...")

        elif prep == 'inspect':
            exqt = ' '.join(exqt)
            if exqt in loc.items:
                print(loc.items.getValue(exqt))
                input("\nPress ENTER to continue...")
            elif exqt in [p.name for p in self.config.places]:
                print(self.config.getVertex(exqt))
                input("\nPress ENTER to continue...")
            elif exqt in loc.npcs:
                print(loc.players.getValue(exqt))
                input("\nPress ENTER to continue...")
            else:
                print("Unable to inspect",exqt)
                time.sleep(2)

        elif prep == 'save':
            if self.config.save():
                print("Successfully saved current game.")
                time.sleep(2)
            else:
                print("Unable to save current game.")
                time.sleep(2)
        
        elif prep == 'quit':
            sys.exit('Exiting program...')

        else:
            print("Unable to interpret commmand.")
            time.sleep(2)
    
        #Final step
        #Update player in BST
        #If not returns for failures were triggered
        key, meta, cargo = self.PC.nodeFromPlayer(name, loc, health, stamina, wt, cb, maxWt, maxCb, inv)
        loc.players.setValue(key, meta, cargo)

        return loc.players.getValue(name) #Return player object for next iteration


