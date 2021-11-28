from endroits import World, Place
from player import Player
from items import Item
from save import *

#List of places
house = World()
kitchen = Place(house, 'kitchen', '')
basement = Place(house, 'basement', '')
hallway = Place(house, 'hallway', '')
bedroom1 = Place(house, 'bedroom1', '')
bedroom2 = Place(house, 'bedroom2', '')
office = Place(house, 'office', '')
livingRoom = Place(house, 'living room', '')
yard = Place(house, 'front yard', '')

#World Map
kitchen.connect(basement)
kitchen.connect(livingRoom)
hallway.connect(livingRoom)
office.connect(hallway)
bedroom1.connect(hallway)
bedroom2.connect(hallway)
livingRoom.connect(yard)

#Cast of Characters
##### = Player(name, desc, health, stamina, location, maxWt, maxCube)
alice = Player('Alice', '', 100, 75, bedroom1, 45, 45)
bob = Player('Bob', '', 100, 90, bedroom2, 45, 45)
bertha = Player('Bertha', '', 100, 50, livingRoom, 45, 45)
Arthur = Player('Arthur', '', 100, 85, livingRoom, 45, 45)

#List of Items
#### = Item(name, weight, cube, desc, location, duplicity, contents)
#Surf gear:
surfboard1 = Item('surfboard', 10, 45, 'THE LOG', basement)
surfboard2 = Item('surfboard', 10, 40, 'THE FISH', office)
wetsuit = Item('wetsuit', 3, 15, 'four-three', basement)
booties = Item('booties', 2, 3, '', basement)
hood = Item('wetsuit hood', 1, 1, '', basement)
wax = Item('surf wax', 1, 0.25, '', office, quantity = 3)
towel = Item('hoodie towel', 3, 5, '', hallway)

#Food:
chips = Item('tortilla chips', 0.5, 3, '', kitchen, quantity = 2)

#Test descriptions:
#print(
#alice.describe(),
#kitchen.describe(),
#surfboard1.describe()
#)

#Test ckpt 
#print(createCheckpoint(house))
