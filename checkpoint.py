import json
from base import GameItem

class Checkpoint:

    def __init__(self, base, inv):
        self.checkBase = self.checkObj(base)
        self.checkInv = self.checkObj(inv)
        self.ckpt = {}

    def checkObj(self, base):
        return lambda x: isinstance(x, base)

    def saveObj(self, obj):
        pass
