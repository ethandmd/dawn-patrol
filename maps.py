class MasterMap:
    top = "     "+"-"*10
    sides = "\n|"+" "*13+"|"
    bottom = "\n"+"-"*15

    def display(self, occ=None):
        if occ:
            return self.top + self.sides*2 + "\n|"+" "*4+"(you)"+" "*4+"|" + self.sides*2 + "\n|" + " "*4+"master"+" "*3 + "|" + self.sides + self.bottom
        else:
            return self.top + self.sides*4 +"\n|" + " "*4 + "master" + " "*3 + "|" + self.sides + self.bottom

class HallwayMap:
    top = " "*4+"-"
    topSide = "|"+" "*5
    pass

