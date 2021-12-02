import os
from datetime import datetime, timedelta
import random

class Controller:

    MURPHY = random.random()

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
        factorM = random.random()
        if factorM <= self.MURPHY:
            return True
        else:
            return False

    def parser(self, arg):
        if len(arg) < 1:
            return

        MURPH_LAW = self.murph()

        cmd = arg.lower().split()
        prepCmd = cmd[0]
        execCmd = cmd[1:]

        if prepCmd == "help":
            self.help()
                
        elif prepCmd == "move":
            for frago in execCmd:
                try:
                    self.player.move(frago)
                    if MURPH_LAW:
                        self.player.injure(self.player.inventory.wt * 0.25 + 10)
                        print("Murph got you.\n-10 health, 10 sec timeout :(")
                        self.timeout(10)

                except KeyError as e:
                    print("Unable to intepret door command for {}.".format(frago))

        elif prepCmd == "pickup":
            if len(execCmd) == 1: 
                execCmd = execCmd[0]
                self.player.takeItem(execCmd)
            else:
                print("Unable to interpret item to pick up.")

        elif prepCmd == "drop":
            if len(execCmd) == 1:
                execCmd = execCmd[0]
                self.player.dropItem(execCmd)
            else:
                print("Unable to interpret item to drop.")

        elif prepCmd == "put":
            if len(execCmd) == 2:
                self.player.putItem(execCmd[0], execCmd[1])
            else:
                print("Unable to interpret location or item.")

        elif prepCmd == "order":
            raise NotImplementedError

        elif prepCmd == "status":
            print(self.player)
            print("\nDoors:")
            for d in self.player.loc.doors:
                print(d)

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
            else:
                print("Unable to find item to inspect.")

        else:
            print("Unable to understand command.")

        input("\nPress ENTER to continue.")

    def prompt(self):
        self.clear()
        cmd = input("Enter command: (help to display menu)\n")
        self.parser(cmd)
