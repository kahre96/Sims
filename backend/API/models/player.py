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
    def __init__(self, empId, ranking, level, xpTotal, xpMonth, last_login, consecutive_days, displayName, birthday_today):
        self.empId          = empId
        self.ranking        = ranking
        self.level          = level
        self.xpTotal        = xpTotal
        self.xpMonth        = xpMonth
        self.last_login     = last_login
        self.consecutive_days=consecutive_days
        self.displayName    = displayName
        self.birthday_today = birthday_today
    
    def getSQLData(self):
        return (self.empId, self.ranking, self.level,self.xpTotal, self.xpMonth, self.last_login, self.consecutive_days) 

    
    def toJSON(self):
        return json.dumps(self, default=json_default, sort_keys=True, indent=4)

'''    def getLatestPlayerId(connection):
        with connection.cursor() as cursor:
            sql = "SELECT player_ID FROM Player ORDER BY player_ID DESC LIMIT 1";
            cursor.execute(sql)
            if cursor.fetchone() is None:
                return 0
            result = formatTupleIntoStr(cursor.fetchone())
            return int(result)
'''

      