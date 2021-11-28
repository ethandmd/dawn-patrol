'''Basic components of all game objects.'''
class GameObject:

    def __init__(self, world, name, info):
        self.world = world
        self.name = name
        self.info = info

    def update(self):
        pass

    def __str__(self):
        desc = {"world" : self.name, "name" : self.name, "info" : self.info}

        return str(desc)
