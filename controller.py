from player import Player
from item import Item
from config import Config

class Controller:
    '''Provide game controls for a game player.'''

    def __init__(self, config):
        self.config = config

<<<<<<< HEAD
    def definePlayer(self, loc, health, stamina, inv):
        #Set up game character for user
        
        name = input("Enter your player name: ").lower()
        self.player =  Player(name, loc, health, stamina, inv) #Define Player obj
        key, meta, cargo = self.player.asNode()
        loc.players.setValue(key, meta, cargo) #Add player obj to loc
=======
    cmds = {
            "help":" (Show help menu)",
            "move":"<door> [follow-ons]",
            "pickup":"<object name>",
            "drop":"<object name>",
            "put":"<place name> <object>",
            "order":"<character> <cmd>",
            "status":"Show player status",
            "inspect":"[character][item][room (inspect current location)]"
            }
    
    def __init__(self, world, player=None):
        self.world = world
        if player:
            self.player = player
        else:
            self.player = self.choosePlayer()

    def choosePlayer(self):
        print()
        self.world.showPlayers()
        print()
        choice = ""
        while choice not in self.world.playerNames:
            choice = input("Enter player name choice: ").lower()
        return self.world.getPlayer(choice)

    def preamble(self):
        self.clear()
        msg = '''
        THE LAST DAWN PATROL.

        You have 5 minutes to collect as much gear as you can fit into the truck to go surfing. Choose your
        player, and search through the house to collect necessary and extraneous items to put in the truck 
        (located in the front yard). Each player has a limited item carrying capacity, based on weight and 
        volume. So, you may need help moving items around the house.
        \n
        At the end of the game, scoring is based on meeting a few conditions:\n
        \t1. You must have all necessary surf gear in the truck.\n
        \t\t (Surfboard, wetsuit, gloves, booties, hood)\n
        \t2. You must have 25 pts worth of food items in the truck.\n
        If you meet the requirments, then every additional item in the truck will increase your score.

        '''
        print(msg)
        print(f"Murphy's Law constant for this game: {self.MURPHY}.")
        input("Press ENTER to begin game...")

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def help(self):
        self.clear()
        print("Available commands:\n")
        for k,v in self.cmds.items():
            print(k,v)


    def timeout(self, amt):
        start = datetime.now()
        delta = timedelta(seconds=amt)
        while datetime.now() < start+delta:
            pass
        self.clear()
>>>>>>> main
    
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
<<<<<<< HEAD
            return True
=======
                
        elif prepCmd == "move":
            for frago in execCmd:
                try:
                    self.player.move(frago)
                    if MURPH_LAW:
                        self.player.injure(self.player.inventory.wt * 0.25 + 10)
                        print("Murph got you: -10 health, 10 sec timeout...")
                        self.timeout(10)
                    print("Succesfully moved to {}.".format(frago))

                except KeyError as e:
                    print("Unable to intepret door command for {}.".format(frago))
            
                time.sleep(2)

        elif prepCmd == "pickup":
            if len(execCmd) == 1: 
                execCmd = execCmd[0]
                success = self.player.takeItem(execCmd)
                if success:
                    print("Succesfully picked up {}.".format(execCmd))
                else:
                    print("Unable to pick up object. Try checking your inventory's weight and cube limits.")
            else:
                print("Unable to interpret item to pick up.")
            time.sleep(2)

        elif prepCmd == "drop":
            if len(execCmd) == 1:
                execCmd = execCmd[0]
                self.player.dropItem(execCmd)
                print("Succesfully dropped {}.".format(execCmd))
            else:
                print("Unable to interpret item to drop.")

            time.sleep(2)

        elif prepCmd == "put":
            if len(execCmd) == 2:
                self.player.putItem(execCmd[0], execCmd[1])
                print("Succefully put {} in {}".format(execCmd[1], execCmd[0]))
            else:
                print("Unable to interpret location or item.")
            time.sleep(2)

        elif prepCmd == "order":
            pass

        elif prepCmd == "status":
            print(self.player)
            #print("Inventory Weight:",str(self.player.inventory.wt)+"/"+str(self.player.maxWt))
            #print("Inventory Cube:",str(self.player.inventory.cb)+"/"+str(self.player.maxCb))
            print("\nDoors:")
            for d in self.player.loc.doors:
                print(d)
            input("\nPress ENTER to continue.")
>>>>>>> main

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
