import json
import datetime

def json_default(value):
        if isinstance(value, datetime.date):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

class Player():
    def __init__(self, emp_id, ranking, level, xpTotal, xpMonth, last_login, consecutive_days, displayName, birthday_today):
        self.emp_id         = emp_id
        self.ranking        = ranking
        self.level          = level
        self.xpTotal        = xpTotal
        self.xpMonth        = xpMonth
        self.last_login     = last_login
        self.consecutive_days=consecutive_days
        self.displayName    = displayName
        self.birthday_today = birthday_today
    
    def getSQLData(self):
        return (self.emp_id, self.ranking, self.level, self.xpTotal, self.xpMonth, self.last_login, self.consecutive_days) 

    def toJSON(self):
        return json.dumps(self, default=json_default, 
            sort_keys=True, indent=4)        

    