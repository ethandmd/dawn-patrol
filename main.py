from datetime import datetime, timedelta
from base import World
from endroits import Place
from trucs import Item
from joueur import Player
from controller import Controller

#World
house = World('house', 'the house')

#Rooms
yard = Place('yard', 'Front Yard', house)
living = Place('living', 'Living Room', house)
dining = Place('dining', 'Dining Room', house)
kitchen = Place('kitchen', 'Kitchen', house)
hallway = Place('hallway', 'Hallway', house)
master = Place('master', 'Master Bedroom', house)
guest = Place('guest', 'Guest Bedroom', house)
stairs = Place('stairs', 'Stairwell', house)
basement = Place('basement', 'Basement', house)

#Connections
yard.connect(living)
living.connect(dining)
kitchen.connect(dining)
dining.connect(hallway)
master.connect(hallway)
guest.connect(hallway)
stairs.connect(kitchen)
basement.connect(stairs)

#Player
alice = Player('Alice', 'A person named Alice.', master, 40,65,100,100)

#Characters
bob = Player('Bob', 'A person named Bob.', guest, 45,185,100,80)
chuck = Player('Chuck', 'A person named Chuck.', living, 105, 120, 100, 100)


#Items
##Food:
for i in range(3):
    Item(name='juanitas', desc='Some tortilla chips by Juanita.', loc=kitchen, wt=0.5, cb=1)
water = Item('water', desc='A reusable, insulated water bottle.', loc=dining,wt=5, cb=1)
ham = Item('ham', desc='A whole half ham, smoked.', loc=kitchen, wt=10, cb=3) 
##Surfing
surfboard = Item('longboard', 'A perfect board for riding out the PNW.', basement,4, 80)
wetsuit = Item('wetsuit', 'A four-three wetsuit, no hood.', basement, 4,6)
duffel = Item('duffel', 'A 60L containment device for the finer things in life.', guest, wt=1, cb=2)
##Truck
truck = Item('Truck', 'A midsize pick-up with a 6-ft bed.', yard, 250,500,1e5,1e4)

#Controller
c = Controller(house)
c.preamble()
start = datetime.now()
delta = timedelta(seconds = 300) #reset time for production

while datetime.now() < start + delta:
    c.prompt()

print("TIME IS UP!!!")
print("Now for the scoring...")
c.scoreCard(truck)
