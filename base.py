class GameItem:

    def __init__(self, name, desc, loc):
        self.name = name
        self.desc = desc
        self.loc = loc

    def __str__(self):
        msg = f"Name: {self.name}\nDescription: {self.desc}"

        return msg
