import unittest
from base import BSTNode
from base import BSTBuilder
from base import BSTree
from base import Vertex

class TestBSTNode(unittest.TestCase):

    def test_simple_node(self):
        test_node = BSTNode('jelly', 'meta', 530)
        self.assertEqual(test_node.key, 'jelly')
        self.assertEqual(test_node.meta, 'meta')
        self.assertEqual(test_node.cargo, 530)
        tSTR = '\nName: jelly\nStatus:  meta\nInventory: 530'
        self.assertEqual(str(test_node), tSTR)

    def test_complex_node(self):
        '''Create a node with a BSTree as its cargo.'''
        #Create bst
        bst = BSTree()
        bst.setValue('b', 'one', 1)
        bst.setValue('a', 'two', 2)
        bst.setValue('c', 'three', 3)

        test_node = BSTNode('k', 'meta',  bst)
        self.assertEqual(test_node.key, 'k')
        self.assertEqual(test_node.meta, 'meta')
        self.assertTrue(isinstance(test_node.cargo, BSTree))

class TestBSTree(unittest.TestCase):
    
    def build_simple_bst(self):
        bst = BSTree()
        bst.setValue('a', 'two', 2)
        bst.setValue('b', 'one', 1)
        bst.setValue('c', 'three', 3)
        return bst

    def test_bst(self):
        bst = self.build_simple_bst()
        self.assertTrue(bst.root.right.key, 'b')
        bst.removeValue('b')
        self.assertTrue(bst.root.right.key, 'c')

    def test_emesis(self):
        bst = self.build_simple_bst()
        preEmesis = {'BSTree': [('a', 'two', 2), ('b', 'one', 1), ('c', 'three', 3)]}
        self.assertEqual(bst.emesis(), preEmesis)
        self.assertTrue(bst.root.key, 'a') #Check quicksort

    def test_simple_rebuild(self):
        bst = self.build_simple_bst()
        B = BSTBuilder()
        tBST = B.build(bst.emesis())
        self.assertEqual(bst.emesis(), tBST.emesis())
        self.assertTrue(tBST.root.key, 'b') #Check quicksort

    def test_complex_rebuild(self):
        bst = self.build_simple_bst()
        cBST = BSTree()
        cBST.setValue('one','a',1)
        cBST.setValue('two','b',bst) #complex cargo
        cBST.setValue('three','c',3)
        preEmesis = {
                'BSTree': [
                    ('one', 'a', 1), 
                    ('three', 'c', 3), 
                    ('two', 'b', {
                        'BSTree': [
                            ('a', 'two', 2), 
                            ('b', 'one', 1), 
                            ('c', 'three', 3)
                            ]
                        }
                        )
                    ]
                }
        B = BSTBuilder()
        tBST = B.build(cBST.emesis())
        self.assertEqual(tBST.emesis(), cBST.emesis())
        self.assertTrue(tBST.root.key, 'three') 

class TestVertex(unittest.TestCase):

    def test_vertex(self):
        #Build players BST
        bst = BSTree()
        bst.setValue('mike', {'health':100}, 111)
        bst.setValue('quinn', {'stamina':15}, 3)
        bst.setValue('guy', {'words':444}, 555)
        #Build example graph vertex set
        kitchen = Vertex('kitchen', bst, None, None)
        dining = Vertex('dining', None, None, None)
        living = Vertex('living', None, None, None)
        #Create edges that span G
        kitchen.drawEdge(living)
        kitchen.drawEdge(dining)
        #Fetch mike
        kitchenMike = kitchen.players.getValue('mike')
        bstMike = bst.getValue('mike')
        
        self.assertTrue(kitchenMike, bstMike)
        self.assertTrue(kitchen.dining.name, 'dining')
        self.assertTrue(living.kitchen.name, 'kitchen')
        self.assertTrue(kitchen.isEdge(living))
        self.assertFalse(living.isEdge(dining))

if __name__ == "__main__":
    unittest.main()
