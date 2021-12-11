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
        self.doors = []

        #Update config
        self.config.addPlace(self)

    def drawEdge(self, vertex):
        '''For both vertices, add reference to each other.'''
        if self.config.addEdge(self.name, vertex.name):
            #Add ref as attr to self
            setattr(self, vertex.name, vertex)
            setattr(vertex, self.name, self)
            if vertex.name not in self.doors:
                self.doors.append(vertex.name)
                vertex.doors.append(vertex.name)
            return
        else:
            return

    def __str__(self):
        msg = "Room: " + self.name
        for door in self.doors:
            msg += "\nDoor to " + door
        msg += "\nPlayers:"
        msg += str(self.players)
        msg += "\nNPCs:"
        msg += str(self.npcs)
        msg += "\nItems:"
        msg += str(self.items)
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
            'items':self.items.emesis()
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
        
        def prettyMeta(meta):
            if meta is not None:
                msg = ''
                for k in meta:
                    msg += "\n"+k+" "+str(meta[k])
                return msg
            else:
                return ''

        meta = prettyMeta(self.meta)
        if not isinstance(self.cargo, BSTree):

            return "\nName: " + self.key + "\nStatus:  " + str(meta) + "\nInventory: " + str(self.cargo)
        else:
            return "\nName: " + self.key + "\nAttributes:  " + str(meta) + "\nInventory: " + str(self.cargo.emesis()["BSTree"])

    #def __repr__(self):
    #    pass

class BSTBuilder:
    '''Utility class to construct a BSTree from the output of BSTree.'''
    def __init__(self):
        self.checkIfBST = lambda cargo: "BSTree" in cargo
    
    def build(self, BSTData):
        buildList = BSTData['BSTree']

        if len(buildList) == 0:
            return BSTree()

        def build_from_list(buildList):
            '''
            Build a BSTree from a python dict: {'BSTree':[data]} where each tuple in data is a BSTNode.
            Example tuple:
                ('key', cargo)
            Since a BSTNode can have another BSTree as cargo, this function checks
            if the cargo is a dictionary with the key 'BSTree'. If so it recurses and creates this nested BSTree.
            '''
            bst = BSTree() #Create empty BSTree wrapper class

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
                return traverse(start.left) + "\n"+ str(start) + traverse(start.right)

        return traverse(self.root)

    def __contains__(self, key):
        return self.getValue(key) is not None
