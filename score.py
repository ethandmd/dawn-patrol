import os
import sqlite3

class ScoreCard:
    '''Compute score at the end of game based on truck inventory.'''

    pointDB = ".scores/points.db"

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
        return [tup[0] for tup in inv.emesis()['BSTree']]

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
        boards = ['longboard', 'thefish']
        wear = ['ripcurlsuit', 'booties', 'surfhood']
        pass


    def writeScore(self, username, numItems,  points):
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


    def __call__(self, inv):
        
        keys = self.parseInventory(inv)
        pointLookup = self.retrievePoints(keys)


