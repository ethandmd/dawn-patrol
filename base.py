class Vertex:
    '''
    Base class for rooms (vertices) in a world (graph := G(V,E)).
    Rooms have a name and possibly players(BSTree), NPCs (BSTree), cargo (BSTree).
    '''
    def __init__(self, config, name, players, npcs, items):
        self.config = config
        self.name = name
        self.players = players
        self.npcs = npcs
        self.items = items
        self.outs = []

        #Update config
        self.config.addPlace(self)

    def drawEdge(self, vertex):
        '''For both vertices, add reference to each other.'''
        #Check if vertices are already connected
        #Add ref as attr to self
        if isinstance(vertex, Vertex):
            setattr(self, vertex.name, vertex)
            setattr(vertex, self.name, self)
            #This keeps track of which attrs are edges and which are cargo
            if vertex.name in self.outs:
                return True
            else:
                vertex.outs.append(self.name)
                self.outs.append(vertex.name)
                return True
        else:
            return False

    def __str__(self):
        msg = "Room: " + self.name
        msg += "\n"+"-"*25
        msg += "\nPlayers: " + str(self.players)
        msg += "\nNPCs: " + str(self.npcs)
        msg += "\nItems: " + str(self.cargo)
        msg += "\n" + "-"*25
        #Get list of all attrs
        attrs = vars(self)
        #Pick out the edges
        for door in self.outs:
            msg += "\nDoor to: " + attrs[door].name

        return msg

    def isEdge(self, v):
        '''Given a vertex, check if vertex has edge to vertex.'''
        if v.name in self.outs:
            return hasattr(self, v.name)
        else:
            return False

    def save(self):
        return {self.name:{
            'players':self.players.emesis(),
            'npcs':self.npcs.emesis(),
            'items':self.items.emesis(),
            'outs':self.outs
                }
            }

class BSTNode:
    '''
    Base class for a node in a binary search tree.
    Inputs:
        key: str (node 'name', general method of identification)
        cargo: [None, BST] (node contents, a node can have another BST as its cargo)
    '''

    def __init__(self, key, meta, cargo):
        self.key = key #String
        self.meta = meta
        self.cargo = cargo #Could be another BST if this node has an 'inventory'.
        self.left = None
        self.right = None

    def __str__(self): #Fix cargo, meta printer
        if not isinstance(self.cargo, BSTree):
            return "\nName: " + self.key + "\nStatus:  " + str(self.meta) + "\nInventory: " + str(self.cargo)
        else:
            return "\nName: " + self.key + "\nStatus:  " + str(self.meta) + "\nInventory: " + str(self.cargo.emesis()["BSTree"])

    #def __repr__(self):
    #    pass

class BSTBuilder:
    '''Utility class to construct a BSTree from the output of BSTree.'''
    def __init__(self):
        self.checkIfBST = lambda cargo: "BSTree" in cargo
    '''
    def partition(self, someList):
        smallers = []
        pivot = someList[len(someList)//2] # pick some value from the list
        largers = []
        for x in someList[1:]:
            if x <= pivot:
                smallers.append(x)
            else:
                largers.append(x)
        return smallers, pivot, largers

    def quickSort(self, someList):
        if len(someList) == 0:
            #Base case when a list is already sorted
            return []
        else: #recurse:
            smaller,pivot,larger = self.partition(someList) #Split list into smaller & larger than pivot
            smallerSorted = self.quickSort(smaller) #quicksort smaller list
            largerSorted = self.quickSort(larger) #quicksort larger list
            return smallerSorted + [pivot] + largerSorted #Combine sorted lists

    def findRoot(self, buildList):
        Given a list of keys (from a BSTree), find the ideal middle key.
        keys = [tup[0] for tup in buildList]
        sortedKeys = self.quickSort(keys) #quicksort
        print("sortedkeys: ", sortedKeys)
        n = len(sortedKeys) #get keys length
        middleKey = sortedKeys[n//2] #Pick middle key out of sorted list
        out = lambda buildList: [tup for tup in buildList if tup[0] == middleKey][0] #Return desired tuple 
        
        return out(buildList)
    '''
    def build(self, BSTData):
        buildList = BSTData['BSTree']

        if len(buildList) == 0:
            return BSTree()
        print()
        print(buildList)

    def addItem(self, item):
        if self.inventory.addItem(item):
            if item.loc is self:
                pass
            else:
                item.loc.removeItem(item)
                item.setLocation(self)

        def build_from_list(buildList):
            '''
            Build a BSTree from a python dict: {'BSTree':[data]} where each tuple in data is a BSTNode.
            Example tuple:
                ('key', cargo)
            Since a BSTNode can have another BSTree as cargo, this function checks
            if the cargo is a dictionary with the key 'BSTree'. If so it recurses and creates this nested BSTree.
            '''
            bst = BSTree() #Create empty BSTree wrapper class
            
            #Find ideal BSTree root
            #first = self.findRoot(buildList)
            #bst.setValue(first[0], first[1], first[2])

            #Extract BSTree data from list
            for tup in buildList:
                key, meta = tup[0], tup[1]
                
                #Check for nested BSTrees
                if type(tup[2]) is dict:
                    if self.checkIfBST(tup[2]):
                        nestedBuildList = tup[2]['BSTree']
                        cargo = build_from_list(nestedBuildList) #Build nested BSTree
                else:
                    cargo = tup[2]
                    
                #Create node in BSTree with key, cargo
                bst.setValue(key, meta, cargo)

            return bst
        
        return build_from_list(buildList)

class BSTree:
    '''Wrapper for a BST with added methods for setting, getting and outputting values.'''
    def __init__(self):
        self.root = None

    def setValue(self, key, meta, cargo):
        slow, fast = None, self.root
        while fast is not None:
            slow = fast
            if key == fast.key:
                fast.cargo = cargo
                return
            elif key < fast.key:
                fast = fast.left
            else:
                fast = fast.right

        newNode = BSTNode(key, meta, cargo)
        if slow is None:
            self.root = newNode
        elif key < slow.key:
            slow.left = newNode
        else:
            slow.right = newNode

    def minValue(self, start):
        '''Get the minimum value from a start point.'''
        if start is None:
            return None

        chase = None
        while start.left is not None:
            chase, start = start, start.left

        return start, chase

    def removeValue(self, key):
        '''Delete a node from BSTree and replace it with minimum right-side node.'''
        #Find parent of node and node to delete
        prev, curr = None, self.root
        while curr is not None:
            if key == curr.key:
                return self.delete(curr, prev)
            elif key < curr.key:
                prev, curr = curr, curr.left
            else:
                prev, curr = curr, curr.right
        
        return False

    def delete(self, curr, prev):
        '''Replace node with its minimum right child.'''
        #If deletion node is a leaf
        if curr.left is None and curr.right is None:
            if prev is None: #Check if curr is root
                self.root = None
            elif curr.key < prev.key:
                prev.left = None
            else:
                prev.right = None
        #If deletion node only has right child
        elif curr.left is None:
            if prev is None: #Check if curr is root
                self.root = curr.right
            elif curr.key < prev.key:
                prev.left = curr.right
            else:
                prev.right = curr.right
        #If deletion node only has left child
        elif curr.right is None:
            if prev is None: #Check if curr is root
                self.root = curr.left
            elif curr.key < prev.key:
                prev.left = curr.left
            else:
                prev.right = curr.left
        #If deletion node has two children
        else:
            repl, chase = self.minValue(curr.right)
            if chase is not None:
                chase.left = None #Remove repl node from it's parent
            
            if prev is None: #Check if root
                repl.left, repl.right = curr.left, curr.right
            elif repl.key < prev.key:
                prev.left = repl
            else:
                prev.right = repl

        return curr
            

    def getValue(self, key):
        check = self.root
        while check is not None:
            if key == check.key:
                return check
            elif key < check.key:
                check = check.left
            else:
                check = check.right
        return None

    def emesis(self):
        '''Regurgitate BSTree contents into:
            {'BSTRee':[...]}.
        '''
        def asList(start):
            if start is None:
                return []
            else:
                #Check if node cargo is a BSTree
                if isinstance(start.cargo, BSTree):
                    cargo = start.cargo.emesis()
                else:
                    cargo = start.cargo
                
                return asList(start.left) + [(start.key, start.meta, cargo)] + asList(start.right)
        
        return {'BSTree':asList(self.root)}

    def isEmpty(self):
        return self.root is None
    
    def __str__(self):
        
        def traverse(start):
            if start is None:
                return ''
            else:
                return traverse(start.left) + str(start) + traverse(start.right)

        return traverse(self.root)

    def __contains__(self, key):
        return self.getValue(key) is not None


class Inventory(BSTree):
    '''
    Wrapper around a BSTree.
    
    Adds weight and cube limits on items.
    Adds pickup / drop / inspect wrappers methods.
    '''

    def __init__(self, maxWt, maxCb):
        BSTree.__init__(self)
        self.wt = 0
        self.cb = 0
        self.maxWt = maxWt
        self.maxCb = maxCb

    def pickup(self, item):
        '''Add item to inventory if it meets wt & cube reqs.'''
        if item.wt + self.wt <= self.maxWt:
            if item.cb + self.cb <= self.maxCb:
                #Set item node data
                key, meta, cargo = item.asNode()
                BSTree.setValue(self, key, meta, cargo)
                self.wt += item.wt
                self.cb += item.cb

                return True
        else:
            return False

    def drop(self, item):
        '''Remove item from inventory.'''
        if item.name in self:
            self.wt-= item.wt
            self.cb -= item.cb
            BSTree.removeValue(item.name)

    def inspect(self):
        return str(self)

