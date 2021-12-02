import os
from datetime import datetime, timedelta
import time
import random

class Controller:

    MURPHY = random.randint(1,25)

    cmds = {
            "help":"Show help menu",
            "move":"<door> [follow-ons]",
            "pickup":"<object name>",
            "drop":"<object name>",
            "put":"<place name> <object>",
            "order":"<character> <cmd>",
            "status":"Show player status",
            "inspect":"[character][item][location]"
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
            choice = input("Enter player name choice:")
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
        \t1. You must have all necessary surf gear\n
        \t\t (Surfboard, wetsuit, gloves, booties, hood)\n
        \t2. You must have some kind of food item\n
        \t3. You must have some kind of beverage\n
        If you meet the requirments (75 pts), then every additional item in the truck will increase your score.

        '''
        print(msg)
        print(f"Game iteration Murph factor: {self.MURPHY}.")
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
    
    def murph(self):
        factorM = random.randint(1,100)
        if factorM <= self.MURPHY:
            return True
        else:
            return False

    def parser(self, arg):
        if len(arg) < 1:
            return
        
        MURPH_LAW = self.murph()
        print("Murph law prob for this round: {}.".format(MURPH_LAW))

        cmd = arg.lower().split()
        prepCmd = cmd[0]
        execCmd = cmd[1:]

        if prepCmd == "help":
            self.help()
            input("Press ENTER to continue...")
                
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
                self.player.takeItem(execCmd)
                print("Succesfully picked up {}.".format(execCmd[0]))
            else:
                print("Unable to interpret item to pick up.")
            time.sleep(2)

        elif prepCmd == "drop":
            if len(execCmd) == 1:
                execCmd = execCmd[0]
                self.player.dropItem(execCmd)
                print("Succesfully dropped {}.".format(execCmd[0]))
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
            raise NotImplementedError

        elif prepCmd == "status":
            print(self.player)
            print("\nDoors:")
            for d in self.player.loc.doors:
                print(d)
            input("\nPress ENTER to continue.")

        elif prepCmd == "inspect":
            if len(execCmd) == 1:
                execCmd = execCmd[0]
                if execCmd == self.player.loc.name: #Location
                    print(self.player.loc)
                elif execCmd in [p.name for p in self.player.loc.players()]: #Player
                    player = self.world.getPlayer(execCmd)
                    print(player)
                elif execCmd in self.player.loc.inventory.names: #Location item
                    item = self.player.loc.inventory.getItem(execCmd)
                    print(item)
                elif execCmd in self.player.inventory.names: #Player item
                    item = self.player.inventory.getItem(execCmd)
                    print(item)
                else:
                    print("Unable to find item to inspect.")
                
                input("Press ENTER to continue.")
            
            else:
                print("Unable to find item to inspect.")

        else:
            print("Unable to understand command.")

    def prompt(self):
        self.clear()
        cmd = input("Enter command: (help to display menu)\n")
        print()
        self.parser(cmd)

    def scoreCard(self, truck):
        score = 0
        for item in ['surfboard', 'wetsuit', 'juanitas']:
            if item in truck.inventory:
                score += 25
        if score < 75:
            print("FAIL.")
        else:
            print("PASS.")