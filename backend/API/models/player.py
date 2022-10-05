import json
import datetime

def formatTupleIntoStr(tuple):
        result = str(tuple)
        for character in ')(,':
                result = result.replace(character, '')
        return result

def json_default(value):
        if isinstance(value, datetime.date):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

class Player():
    def __init__(self, playerId, empId, xpTotal, xpMonth, level, last_login, consecutive_days, displayName):
        self.playerId       = playerId
        self.empId          = empId
        self.xpTotal        = xpTotal
        self.xpMonth        = xpMonth
        self.level          = level
        self.last_login     = last_login
        self.consecutive_days=consecutive_days
        self.displayName    = displayName
    
    def getSQLData(self):
        return (self.playerId ,self.empId, self.xpTotal, self.xpMonth, self.level, self.last_login, self.consecutive_days) 

    def getLatestPlayerId(connection):
        with connection.cursor() as cursor:
            sql = "SELECT player_ID FROM Player ORDER BY player_ID DESC LIMIT 1";
            cursor.execute(sql)
            result = formatTupleIntoStr(cursor.fetchone())
            return int(result)

    
    def toJSON(self):
        return json.dumps(self, default=json_default, 
            sort_keys=True, indent=4)        

    