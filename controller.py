import time
import sys

class Controller:
    '''Provide game controls for a game player.'''

    def __init__(self, config, PlayerControl):
        self.config = config
        self.PC = PlayerControl()
    
    def convertToVertex(self, name):
        '''Take a location string and return node in 'world' graph.'''
        for place in self.config.places:
            if name == place.name:
                return place

    def welfareCheck(self, player):
        '''Check player's health and stamina.'''
        if player.meta['health'] <= 0:
            return 'health'
        elif player.meta['stamina'] <= 0:
            return 'stamina'
        else:
            return 

    def parser(self, player, arg):
        '''Essential utility function for taking user input and translating it to game actions.'''
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
                    wt += item.meta['wt']
                    cb += item.meta['cb']
                    loc.items.removeValue(item.key)
                    print("Successfully picked up",exqt)
                    time.sleep(1)
                else:
                    print("Unable to pickup",exqt,"check your inventory weight and cube limits.")
            else:
                print("Unable to pickup",exqt)
                time.sleep(1)
        ##drop
        elif prep == 'drop':
            exqt = ' '.join(exqt)
            #Find out if an item called exqt exists
            item = inv.getValue(exqt)
            if item is not None:
                wt -= item.meta['wt']
                cb -= item.meta['cb']
                if wt < 0:
                    wt = 0
                if cb < 0:
                    cb = 0
                inv.removeValue(item.key)
                loc.items.setValue(item.key, item.meta, item.cargo)
                print("Successfully dropped", exqt)
                time.sleep(1)
            else:
                print("Unable to drop",exqt)
                time.sleep(1)
        ##put
        elif prep == 'put':
            #Check  exqt1 & exqt2
            try:
                #Get raw item and recipient
                item, recipient = inv.getValue(exqt[0]), loc.items.getValue(exqt[1])
                #Put item
                if self.PC.putItem(item, recipient):
                    #Drop item
                    wt -= item.meta['wt']
                    cb -= item.meta['cb']
                    if wt < 0:
                        wt = 0
                    if cb < 0:
                        cb = 0
                    inv.removeValue(item.key)

                    print("Succesfully put",item.key,"in",recipient.key)
                    time.sleep(1)
                else:
                    print("Unable to put",item.key,"in",recipient.key)
                    time.sleep(1)

            except (TypeError, AttributeError, IndexError) as e:
                print(e)
                print("Unable to process 'put' command.")
                time.sleep(1)

        ##takeout
        elif prep == 'takeout':
            try:
                #Get giver and item
                giver = loc.items.getValue(exqt[1])
                item = giver.cargo.getValue(exqt[0])
                #Take item from giver
                loc.items.setValue(item.key, item.meta, item.cargo)
                giver.cargo.removeValue(item.key)
                print("Successfully removed",exqt[0],"from",exqt[1])
                time.sleep(1)
            except (AttributeError, TypeError, IndexError) as e:
                print(e)
                print("Unable to take",exqt[0],"from",exqt[1])
                time.sleep(1)
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
                if name in ['chuck','larry']: #Check for NPC ##Temp solution
                    loc.npcs.removeValue(name)
                else:
                    loc.players.removeValue(name) #Remove player from old loc
                loc = newLoc #Update loc
                stamina = self.PC.exert(stamina, wt*0.1+2)
                print("Successfully moved to",loc.name)
                time.sleep(1)
            else:
                print("Unable to move to",exqt)
                time.sleep(1)

        ##order
        elif prep == 'order':
            try:
                #Find player
                sub = loc.npcs.getValue(exqt[0])
                if sub is not None:
                    newCmd = ' '.join(exqt[1:])
                    
                    #Run command input system on NPC
                    nkey, nmeta, ncargo, nloc = self.parser(sub, newCmd)
                    self.packageTurn(nkey, nmeta, ncargo, nloc)

                    print("Successfully ordered",sub.key,"to",newCmd)
                    time.sleep(1)
                else:
                    print("Unable to order this person")
                    time.sleep(1)

            except (TypeError, AttributeError, IndexError) as e:
                #print(e)
                print("Unable to perform order command.")
                time.sleep(1)

        ##status
        elif prep == 'status':
            print(self.PC.asString(name, loc, health, stamina, wt, cb, maxWt, maxCb, inv))
            input("\nPress ENTER to continue...")

        elif prep == 'inspect':
            exqt = ' '.join(exqt)
            if exqt in loc.items:
                item = loc.items.getValue(exqt)
                print(item)
                input("\nPress ENTER to continue...")
            elif exqt == 'room':
                print(loc)
                input("\nPress ENTER to continue...")
            elif exqt in loc.npcs:
                npc = loc.npcs.getValue(exqt)
                nname, nloc, nhealth, nstamina, nwt, ncb, nmaxWt, nmaxCb, ninv = self.PC.playerFromNode(npc)
                nloc = self.convertToVertex(nloc)
                print(self.PC.asString(nname, nloc, nhealth, nstamina, nwt, ncb, nmaxWt, nmaxCb, ninv))
                input("\nPress ENTER to continue...")
            else:
                print("Unable to inspect",exqt)
                time.sleep(1)

        elif prep == 'save':
            if self.config.save():
                print("Successfully saved current game.")
                time.sleep(1)
            else:
                print("Unable to save current game.")
                time.sleep(1)
        
        elif prep == 'quit':
            sys.exit('Exiting program...')

        else:
            print("Unable to interpret commmand.")
            time.sleep(1)
    
        #Final step
        #Update player in BST
        #If not returns for failures were triggered
        key, meta, cargo = self.PC.nodeFromPlayer(name, loc, health, stamina, wt, cb, maxWt, maxCb, inv)
        
        return key, meta, cargo, loc

    def packageTurn(self, key, meta, cargo, loc):
        '''Upate player in game 'world' so that game can be saved at any point.'''
        #Check for NPC ##Temp solution
        if key in ['chuck','larry']:
            loc.npcs.setValue(key,meta,cargo)
            return
        else:
            loc.players.setValue(key, meta, cargo)
            return loc.players.getValue(key) #Return player object for next iteration


