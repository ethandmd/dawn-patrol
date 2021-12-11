class Item:

    def __init__(self, name, wt, cb, inv):
        self.name = name
        self.wt = wt
        self.cb = cb
        self.inv = inv

    def asNode(self):
        key = self.name
        meta = {'wt':self.wt, 'cb':self.cb}
        cargo = self.inv

        return key, meta, cargo
