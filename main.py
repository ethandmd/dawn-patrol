import sys
import threading
from base import BSTree, Vertex
from config import Config
from controller import Controller
from player import Player
from datetime import datetime, timedelta

#######
#Game Prompt
#######
'''
def runningTime():
    while True:
        print("Time left: "+str((start+timeLeft)-datetime.now())+"\r", end="")
'''

def loadPreamble():
    with open(config.preambleFP, 'r') as f:
        print('\033[95m'+f.read()+'\033[0m')

#######
#Config
#######

config = Config()
controller = Controller(config, Player)

##############
#Pre-Game menu:
###############
config.clear()
print('\033[92;4;1m'"Welcome to The Last Dawn Patrol!"+'\033[0m')
print()
choice = None
while choice not in ['y','n']:
    choice = input("Would you like to start a new game ([y]/[n])?: ").lower()
if choice[0] == 'y':
    loadPreamble()
    #Prep game env
    player, timeLeft = config.loadGame('vanilla') #Load vanilla game, return player and timedelta
    
else:
    print("Loading most recently saved game checkpoint...")
    player, timeLeft = config.loadGame() #Load most recently saved ckpt json file

if player is None:
    #Customize name from default
    name = None
    while name is None:
        name = input("Enter your desired username: ").lower()
    master = config.getVertex('master')
    master.players.setValue(name, {'loc':master.name, 'health':100, 'stamina':100,'wt':0, 'cb':0, 'maxWt':50, 'maxCb':75}, BSTree())
    player = master.players.getValue(name)

##########
#Game Play
##########
start = datetime.now()

#printThread = threading.Thread(target=runningTime)
#printThread.start()

gameon = True

while gameon:
    config.clear()
    print('THE LAST DAWN PATROL')
    config.updateTime((start+timeLeft)-datetime.now()) #Calculate remaining time
    config.displayHelp()
    print()
    if datetime.now() <= start + timeLeft:
        print("Time left:",(start+timeLeft)-datetime.now())
        arg = input("Enter command: \n") #Take user input
        key, meta, cargo, loc = controller.parser(player, arg) #Get updated attrs for player
        player = controller.packageTurn(key, meta, cargo, loc) #Update player attrs in BSTree
    else:
        gameon = False

#promptThread = threading.Thread(target=prompt)
#promptThread.run()

print('\033[91m'+"Time is up!"+'\033[0m')
config.scoreCard(player.key, player.cargo) #Calculate score
