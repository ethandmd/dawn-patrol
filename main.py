from base import *
from config import Config
from controller import Controller

#Config
config = Config()

#Places
kitchen = Vertex(config, 'kitchen', BSTree(), BSTree(), BSTree())
dining = Vertex(config, 'dining', BSTree(), BSTree(), BSTree())
living = Vertex(config, 'living', BSTree(), BSTree(), BSTree())
master = Vertex(config, 'master', BSTree(), BSTree(), BSTree())
guest = Vertex(config, 'master', BSTree(), BSTree(), BSTree())
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
