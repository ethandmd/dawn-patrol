from base import BSTree, Vertex
from config import Config
from controller import Controller
from player import Player
from datetime import datetime, timedelta

#Config
config = Config()
controller = Controller(config, Player)

#Places
kitchen = Vertex(config, 'kitchen', BSTree(), BSTree(), BSTree())
foyer = Vertex(config, 'foyer', BSTree(), BSTree(), BSTree())
master = Vertex(config, 'master', BSTree(), BSTree(), BSTree())
office = Vertex(config, 'office', BSTree(), BSTree(), BSTree())
bathroom = Vertex(config, 'bathroom', BSTree(), BSTree(), BSTree())
hallway = Vertex(config, 'hallway', BSTree(), BSTree(), BSTree())
stairs = Vertex(config, 'stairs', BSTree(), BSTree(), BSTree())
basement = Vertex(config, 'basement', BSTree(), BSTree(), BSTree())
frontyard = Vertex(config, 'frontyard', BSTree(), BSTree(), BSTree())
backyard = Vertex(config, 'backyard', BSTree(), BSTree(), BSTree())

master.drawEdge(hallway)
office.drawEdge(hallway)
bathroom.drawEdge(hallway)
hallway.drawEdge(foyer)
kitchen.drawEdge(foyer)
foyer.drawEdge(frontyard)
stairs.drawEdge(kitchen)
backyard.drawEdge(stairs)
basement.drawEdge(stairs)


#Characters
#Larry has a scarf
linv = BSTree()
linv.setValue('scarf', {'wt':1, 'cb':1}, None)

kitchen.npcs.setValue('larry', {'loc':kitchen.name, 'health':100, 'stamina':100, 'wt':0, 'cb':0, 'maxWt':50, 'maxCb':75}, linv)
foyer.npcs.setValue('chuck', {'loc':foyer.name, 'health':100, 'stamina':100, 'wt':0, 'cb':0, 'maxWt':50, 'maxCb':75}, BSTree())
master.players.setValue('USERNAME', {'loc':master.name, 'health':100, 'stamina':100,'wt':0, 'cb':0, 'maxWt':50, 'maxCb':75}, BSTree())


#Items
##Kitchen
kitchen.items.setValue('chips', {'wt':1,'cb':2}, None)
kitchen.items.setValue('jelly', {'wt':4,'cb':2}, None)
kitchen.items.setValue('apple', {'wt':1,'cb':1}, None)
kitchen.items.setValue('coffee', {'wt':3, 'cb':2}, None)

##Foyer
foyer.items.setValue('solarcharger', {'wt':1,'cb':2}, None)
foyer.items.setValue('puffyjacket', {'wt':1,'cb':5}, None)

##Master
#Socks got $$$
sinv = BSTree()
sinv.setValue('20dollars', {'wt':0, 'cb':0}, None)
master.items.setValue('woolsocks', {'wt':1,'cb':1}, sinv)

##Office
office.items.setValue('thefish',{'wt':9, 'cb':30}, None)
office.items.setValue('wallet', {'wt':1, 'cb':1}, None)
office.items.setValue('hoodedtowel', {'wt':5, 'cb':8}, None)
office.items.setValue('kalilinux', {'wt':2, 'cb':2}, None)

##Bathroom
bathroom.items.setValue('toiletpaper', {'wt':1, 'cb':2}, None)
bathroom.items.setValue('toothbrush', {'wt':2, 'cb':1}, None)

##Hallway
hallway.items.setValue('surfhood', {'wt':2,'cb':3}, None)

##Stairs

##Basement
#Pack has booties in it
pinv = BSTree()
pinv.setValue('booties',{'wt':2,'cb':4}, None)
basement.items.setValue('pack', {'wt':5, 'cb':25}, BSTree())
basement.items.setValue('longboard', {'wt':10, 'cb':70}, None)
basement.items.setValue('snowboard', {'wt':8, 'cb':40}, None)
basement.items.setValue('ripcurlsuit', {'wt':3, 'cb':10}, None)

##Frontyard
#Truck has a big inv
frontyard.items.setValue('truck',{'wt':5000, 'cb':10000}, BSTree())

##Backyard
backyard.items.setValue('sitka', {'wt':55, 'cb':60}, None) #Sitka!!
backyard.items.setValue('trailwagon', {'wt':20, 'cb':50}, BSTree())

config.save()

###############
#Pre-Game menu:
###############
config.clear()
print()
print("Welcome to The Last Dawn Patrol...")
choice = input("Would you like to start a new game ([y]/[n])?: ").lower()
if choice[0] == 'y':
    #Prep game env
    player, timeLeft = config.loadGame('vanilla') #Load vanilla game, return player and timedelta
else:
    print("Loading most recently saved game checkpoint...")
    player, timeLeft = config.loadGame() #Load most recently saved ckpt json file

if player.key == 'USERNAME':
    #Customize name from default
    name = None
    while name is None:
        name = input("Enter your desired username: ").lower()
    player.key = name #Update player name value
    
##########
#Game Play
##########
start = datetime.now()
while datetime.now() < start + timeLeft:
    print('THE LAST DAWN PATROL')
    print()
    config.clear()
    config.updateTime((start+timeLeft)-datetime.now()) #Calculate remaining time
    #config.updateTime(timeLeft) #Update remaining time in config
    print("Time left:",(start+timeLeft)-datetime.now()) #Display remaining time (static)
    arg = input("Enter command: \n") #Take user input
    key, meta, cargo, loc = controller.parser(player, arg) #Get updated attrs for player
    player = controller.packageTurn(key, meta, cargo, loc) #Update player attrs in BSTree

print("GAME OVER")
