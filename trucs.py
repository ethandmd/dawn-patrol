'''In-game items'''
from base import GameItem, Inventory

class Item(GameItem):
    '''Item base class'''

    def __init__(self, name, desc, loc, maxWt, maxCb, wt, cb):
        GameItem.__init__(self, name, desc, loc, maxWt, maxCb)
        self.wt = wt
        self.cb = cb

        self.loc.addItem(self)

    def __str__(self):
        msg = GameItem.__str__(self)

        #Add attributes unique to this class
        msg += f"\nWeight: {self.wt}, Cube: {self.cb}"
        return msg
