import os
import sqlite3

class ScoreCard:
    '''Compute score at the end of game based on truck inventory.'''

    pointDB = ".scores/points.db"
    boards = ['longboard', 'shortboard']
    wear = 'ripcurlsuit'
    food = ['chips','jelly','apple','coffee']
    ogpts = [
            ('chips', 5),
            ('apple', 3),
            ('jelly', 1),
            ('coffee', 10),
            ('solarcharger',7),
            ('puffyjacket', 7),
            ('woolsocks', 9),
            ('shorboard',21),
            ('longboard',25),
            ('wallet', 5),
            ('hoodedtowel', 10),
            ('kalilinux',0),
            ('toiletpaper',1),
            ('toothbrush',2),
            ('surfhood',15),
            ('pack',2),
            ('booties',20),
            ('snowboard',0),
            ('ripcurlsuit',25),
            ('sitka',50),
            ('trailwagon',15)
            ]


    def __init__(self):
        '''inv : truck.cargo (BSTree)'''
        #if not os.path.exists(self.pointDB):
        #    print("Missing point lookup database!")
        #raise NotImplementedError
        if self.pointDB is None:
            raise NotImplementedError
        else:
            pass

    def parseInventory(self, inv):
        '''Retrieve the name of each item in the jackpot.'''
        keys = []
        for tup in inv.emesis()['BSTree']:
            if tup[2] is not None: #Check if an item had nested items
                for ntup in tup[0]:
                    keys.append(ntup[0])
                else:
                    keys.append(tup[0])

        return keys

    def viewHighSCore(self):
        try:
            conn = sqlite3.connect(self.pointDB)
            cur = conn.cursor()

            cur.execute("SELECT * FROM scores ORDER BY points")
            res = cur.fetchone()
            print("Highest score:")
            for i in res:
                print(i, end=" ")
        except sqlite3.Error as e:
            print(e)
            return False

    def retrievePoints(self, keys):
        '''Find out how much each item in inv is worth.'''
        pointLookup = {}

        try:
            conn = sqlite3.connect(self.pointDB) #Open connection to point lookup DB
            cur = conn.cursor() #Init cursor obj

            for key in keys:
                cur.execute('SELECT points FROM pointlookup WHERE name = (?)',(key,))
                res = cur.fetchone()
                pointLookup[key] = res[0]
                conn.close()

            return pointLookup

        except sqlite3.Error as e:
            print(e)
            return False

    def writeOriginalPoints(self, data):
        '''
        Write data: list of tuples, to pointlookup table.
        To be used with Config.createGame().
        '''

        try:
            conn = sqlite3.connect(self.pointDB)
            cur = conn.cursor()
            cur.execute("CREATE TABLE pointlookup (name, points)")
            cur.executemany("INSERT INTO pointlookup VALUES (?, ?)", data)
            conn.commit()
            conn.close()
            return True

        except sqlite3.Error as e:
            print(e)
            return False

    def calculateScore(self, pointLookup):
        #Needed surf gear to win: 
        if self.boards[0] in pointLookup or self.boards[1] in pointLookup: #Check for a surfboard
            if self.wear in pointLookup:
                if self.food[0] in pointLookup or self.food[1] in pointLookup or self.food[2] in pointLookup or self.food[3] in pointLookup:
                    points = sum(list(pointLookup.values()))

                    return points

    def writeScore(self, username, numItems, points):
        '''
        Used to record game scores.
        '''
        try:
            conn = sqlite3.connect(self.pointDB)
            cur = conn.cursor()
            cur.execute("INSERT INTO scores VALUES (?, ?, ?)", (username, numItems, points))
            conn.commit()
            conn.close()
            print("Successfully saved score.")
            return True
        
        except sqlite3.Error as e:
            print(e)
            return False


    def __call__(self, username, inv):
        
        keys = self.parseInventory(inv)
        pointLookup = self.retrievePoints(keys)
        score = self.calculateScore(pointLookup)
        if score is not None:
            self.writeScore(username, len(keys), score)
        print("Your score is",score)

        return


