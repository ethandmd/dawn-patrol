from base import *
from config import Config
from controller import Controller
from player import Player
from datetime import datetime, timedelta

#Config
config = Config()
controller = Controller(config, Player)
'''
#Places
kitchen = Vertex(config, 'kitchen', BSTree(), BSTree(), BSTree())
dining = Vertex(config, 'den', BSTree(), BSTree(), BSTree())
living = Vertex(config, 'foyer', BSTree(), BSTree(), BSTree())
master = Vertex(config, 'master', BSTree(), BSTree(), BSTree())
guest = Vertex(config, 'backroom', BSTree(), BSTree(), BSTree())
bathroom = Vertex(config, 'bathroom', BSTree(), BSTree(), BSTree())
hallway = Vertex(config, 'hallway', BSTree(), BSTree(), BSTree())
stairs = Vertex(config, 'stairs', BSTree(), BSTree(), BSTree())
basement = Vertex(config, 'basement', BSTree(), BSTree(), BSTree())
frontyard = Vertex(config, 'frontyard', BSTree(), BSTree(), BSTree())
backyard = Vertex(config, 'backyard', BSTree(), BSTree(), BSTree())

master.drawEdge(hallway)
guest.drawEdge(hallway)
bathroom.drawEdge(hallway)
hallway.drawEdge(dining)
kitchen.drawEdge(dining)
dining.drawEdge(living)
living.drawEdge(frontyard)
stairs.drawEdge(kitchen)
backyard.drawEdge(stairs)
basement.drawEdge(stairs)


#Characters
linv = BSTree()
linv.setValue('scarf', {'wt':1, 'cb':1}, None)
kitchen.npcs.setValue('larry', {'loc':kitchen.name, 'health':100, 'stamina':100, 'wt':0, 'cb':0, 'maxWt':50, 'maxCb':75}, linv)
kitchen.npcs.setValue('chuck', {'loc':kitchen.name, 'health':100, 'stamina':100, 'wt':0, 'cb':0, 'maxWt':50, 'maxCb':75}, BSTree())
dining.players.setValue('ethan', {'loc':dining.name, 'health':100, 'stamina':100,'wt':0, 'cb':0, 'maxWt':50, 'maxCb':75}, BSTree())


#Items
kitchen.items.setValue('chips', {'wt':1,'cb':2}, None)
kitchen.items.setValue('jelly', {'wt':2,'cb':1}, None)
kitchen.items.setValue('apple', {'wt':1,'cb':1}, None)
dining.items.setValue('pack', {'wt':5, 'cb':25}, BSTree())

config.save()
'''
#Player
player, timeLeft = config.loadGame() #Load most recent game ckpt, return player and timedelta

#Game Play
start = datetime.now()
while datetime.now() < start + timeLeft:
    config.clear()
    config.updateTime((start+timeLeft)-datetime.now()) #Calculate remaining time
    #config.updateTime(timeLeft) #Update remaining time in config
    print("Time left:",(start+timeLeft)-datetime.now()) #Display remaining time (static)
    arg = input("Enter command: \n") #Take user input
    key, meta, cargo, loc = controller.parser(player, arg) #Get updated attrs for player
    player = controller.packageTurn(key, meta, cargo, loc) #Update player attrs in BSTree

print("GAME OVER")
