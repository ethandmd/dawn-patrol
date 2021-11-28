class GameItem:

    def __init__(self, name, desc, loc):
        self.name = name
        self.desc = desc
        self.loc = loc

    def __str__(self):
        msg = f"Name: {self.name}\nDescription: {self.desc}"

        return msg

    def save(self):
        '''Method for saving game items.'''
        
        return {self.name : {'desc': self.desc, 'loc':self.loc.name}}