class Map:

    top = ' '*10 + 'backyard'
    btop = '\n              |'
    mtop = "\n   kitchen -- stairs -- basement"
    tm = "\n     |"
    m = "\n     |        office"
    mm = "\n     |         |"
    mmm = "\n     |         |"
    middle = "\n   foyer -- hallway -- bathroom"
    b = "\n     |         |"
    bb = "\n     |       master"
    bottom = "\n   frontyard"

    def __str__(self):
        return self.top+self.btop+self.mtop+self.tm+self.m+self.mm+self.mmm+self.middle+self.b+self.bb+self.bottom

