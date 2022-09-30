

def formatTupleIntoStr(tuple):
        result = str(tuple)
        for character in ')(,':
                result = result.replace(character, '')
        return result

class Player():
    def __init__(self, playerId, empId, rank, displayName, xpTotal, xpMonth, level):
        self.playerId       = playerId
        self.empId          = empId
        self.rank           = rank
        self.displayName    = displayName
        self.xpTotal        = xpTotal
        self.xpMonth        = xpMonth
        self.level          = level
    
    def getSQLData(self):
        return (self.playerId ,self.empId, self.rank, self.xpTotal, self.xpMonth, self.level) 

    def getLatestPlayerId(connection):
        with connection.cursor() as cursor:
            sql = "SELECT Player_ID FROM Player ORDER BY Player_ID DESC LIMIT 1";
            cursor.execute(sql)
            result = formatTupleIntoStr(cursor.fetchone())
            return int(result)