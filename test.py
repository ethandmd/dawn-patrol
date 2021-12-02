from base import World
from endroits import Place
from trucs import Item
from joueur import Player

#World
house = World('house')

#Rooms
yard = Place('front yard', 'A space for looking out.', house)
living = Place('living room', 'A room for livin in.', house)
dining = Place('dining room', 'A room for dining in.', house)
kitchen = Place('living room', 'A room for cooking in.', house)
hallway = Place('hallway', 'A space for walking in.', house)
master = Place('master bedroom', 'A big room for sleeping in.', house)
guest = Place('guest bedroom', 'A smaller room for sleeping in.', house)
stairs = Place('stairwell', 'A space for (a/de)scending in.', house)
basement = Place('basement', 'A space for doing activities in.', house)

#Connections
yard.connect(living)
living.connect(dining)
dining.connect(kitchen)
dining.connect(hallway)
master.connect(hallway)
guest.connect(hallway)
stairs.connect(kitchen)
basement.connect(stairs)

#Player
alice = Player('Alice', 'A person named Alice.', master, 40,65,100,100)

#Characters
bob = Player('Bob', 'A person named Bob.', guest, 45,85,100,80)
chuck = Player('Chuck', 'A person named Chuck.', living, 105, 120, 100, 100)


#Items

##Food:
for i in range(5):
    Item(name='Juanitas', desc='Some tortilla chips by Juanita.', loc=kitchen, maxWt=0, maxCb=0, wt=0.5, cb=1)

surfboard = Item('Waverunner eight-oh', 'A perfect board for riding out the PNW.', basement, 0,0, 4, 80)
wetsuit = Item('wetsuit', 'A four-three wetsuit, no hood.', basement, 0,0,4,6)
duffel = Item('duffel bag', 'A 60L containment device for the finer things in life.', guest, 30, 35, wt=1, cb=2)
truck = Item('The Truck', 'A midsize pick-up with a 6-ft bed.', yard, 250,500,1e5,1e4)
