# Development Diary

## Logs

### 12/09
It's late. I added a Vertex class, added some more unit tests (still from complete, but it gets the gist), and tweaked 
several base class methods. I began implementing classes for Player, PlayerInventory, as well as a controller class. 
Ultimately I got stuck on writing an algorithm to remove a node from a BST, this is where I'll start tomorrow.

TO-DO:
-Add removeItem method to BSTree
-Finish player, player inventory, & item classes
-Finish controller class

### 12/08
It's late. I built three base classes: BSTNode, BSTree, and BSTBuilder. I am most excited about the BSTBuilder, I think
it will allow me to easily serialize data to JSON format and create game checkpoints. I plan to have an undirected, connected graph representing the game world with ```V(G) := rooms```, and ```E(G) := doors```. Then each room (vertex) will have a 
reference to PLAYERS (BSTree of players in that room) and ITEMS (BSTree of items in that room). How I've constructed it, it
so each node in the BSTree can have another BSTree as the node's cargo. This is to represent a player or item having an "inventory". 

TO-DO:
-I need to finish writing the tests for these three classes and their methods. So far so good on my back-of-the-napkin tests.
-I need to build subclasses of the BSTNode class for PLAYER and ITEM.

I didn't necessarily plan well for subclassing. Perhaps I need to add some kind of 'metadata' attr to the BSTNode class and
reflect that in my BSTBuilder and BSTree wrapper class. This way I can maintain some kind of record of player health, etc...

-I need to create a WORLD (a graph ```G := G(V,E)``` representing the graph of the rooms.

After these 3 tasks are complete and tested I can introduce the save-game feature relatively easily and tune the rest of the
gameplay components. The above three tasks should take me a few hours. Let's try to complete a v0.1 of this by Saturday am.
