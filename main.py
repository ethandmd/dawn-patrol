import sys
import time
import threading
from base import BSTree, Vertex
from config import Config
from controller import Controller
from player import Player
from datetime import datetime, timedelta

#######
#Game Prompt
#######

#def runningTime():
#    while True:
#        print("Time left: "+str((start+timeLeft)-datetime.now())+"\r", end="")


def loadPreamble(config):
    with open(config.preambleFP, 'r') as f:
        print('\033[95m'+f.read()+'\033[0m')

#######
#Config
#######
def setup():
    config = Config()
    controller = Controller(config, Player)

    #Pre-Game menu:

    config.clear()
    print('\033[92;4;1m'"Welcome to The Last Dawn Patrol!"+'\033[0m')
    print()
    choice = config.gameChoice()

    if choice == 'newGame':
        loadPreamble(config)
        #Prep game env
        player, timeLeft = config.loadGame('vanilla') #Load vanilla game, return player and timedelta
    
    else:
        print("Loading most recently saved game checkpoint...")
        print("Game on!")
        player, timeLeft = config.loadGame() #Load most recently saved ckpt json file

    if player is None:
        #Customize name from default
        name = None
        while name is None:
            name = input("Enter your desired username: ").lower()
        master = config.getVertex('master')
        master.players.setValue(name, {'loc':master.name, 'health':100, 'stamina':100,'wt':0, 'cb':0, 'maxWt':50, 'maxCb':75}, BSTree())
        player = master.players.getValue(name)

    return config, controller, player, timeLeft

##########
#Game Play
##########
if __name__ == "__main__":

    config, controller, player, timeLeft = setup()

    start = datetime.now()

    #printThread = threading.Thread(target=runningTime)
    #printThread.start()

    gameon = True

    while gameon:
        config.clear()
        print('THE LAST DAWN PATROL')
        config.updateTime((start+timeLeft)-datetime.now()) #Calculate remaining time
        print()
        config.displayHelp()
        print()
        if datetime.now() <= start + timeLeft:
            print("Time left:",(start+timeLeft)-datetime.now())
        
            welfare = controller.welfareCheck(player)
            if welfare == 'health':
                gameon = False
                print("Game over, you died.")
            elif welfare == 'stamina':
                print("No stamina. You need to rest.")
                print("For every second of rest you regain 1 point of stamina.")
                secs = config.getRestTime()
                print("Resting for",secs,"seconds.")
                time.sleep(secs)
                player.meta['stamina'] += secs
            else:

                arg = input("Enter command: \n") #Take user input
                key, meta, cargo, loc = controller.parser(player, arg) #Get updated attrs for player
                player = controller.packageTurn(key, meta, cargo, loc) #Update player attrs in BSTree
        else:
            gameon = False
            print('\033[91m'+"Time is up!"+'\033[0m')

    #promptThread = threading.Thread(target=prompt)
    #promptThread.run()
    frontyard = config.getVertex('frontyard')#Get truck for score calculation
    truck = frontyard.items.getValue('truck')
    config.scoreCard.giveScore(player.key, truck.cargo) #Calculate score

    print("Current Leaderboard:")
    config.scoreCard.viewLeaderboard()
    input("Press ENTER to continue...")
    print()
    print("Thanks for playing!")
    sys.exit("Exiting game...")
