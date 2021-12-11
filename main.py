from base import *
from player import Player
from item import Item
from config import Config
from controller import Controller

#Config
config = Config()

#Places
kitchen = Vertex(config, 'kitchen', BSTree(), BSTree(), BSTree())
dining = Vertex(config, 'dining', BSTree(), BSTree(), BSTree())
living = Vertex(config, 'living', BSTree(), BSTree(), BSTree())

kitchen.drawEdge(dining)
dining.drawEdge(living)

#NPCs
larry = Player('larry', living, 100, 100, Inventory(100,100))
chuck = Player('chuck', living, 100,100, Inventory(100,100))

for p in [larry, chuck]:
    key, meta, cargo = p.asNode()
    living.npcs.setValue(key, meta, cargo)

#Items
chips = Item('chips', 1,2, None)
jelly = Item('jelly', 2,1, None)
apple = Item('apple', 1,1, None)
pack = Item('pack', 5,5, Inventory(50,500))

for i in [chips, jelly, apple]:
    key, meta, cargo = i.asNode()
    kitchen.items.setValue(key, meta, cargo)

key, meta, cargo = pack.asNode()
living.items.setValue(key, meta, cargo)

#Player
control = Controller(config)
control.definePlayer(kitchen, 100, 100, BSTree())
