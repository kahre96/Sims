import json
import datetime

def json_default(value):
        if isinstance(value, datetime.date):
            return dict(year=value.year, month=value.month, day=value.day)
        else:
            return value.__dict__

class Player():
    def __init__(self, emp_id,level, xpTotal, xpMonth, last_login, consecutive_days, displayName, birthday_today):
        self.emp_id         = emp_id
        self.level          = level
        self.xpTotal        = xpTotal
        self.xpMonth        = xpMonth
        self.last_login     = last_login
        self.consecutive_days=consecutive_days
        self.displayName    = displayName
        self.birthday_today = birthday_today
        self.greeting       = "Hej"
        self.xpLevel        = 0
        self.xpNextLevel    = 0
        self.xpGained       = 0
    
    def getSQLData(self):
        return (self.emp_id, self.level, self.xpTotal, self.xpMonth, self.last_login, self.consecutive_days) 


    def toJSON(self):
        return json.dumps(self, default=json_default, 
            sort_keys=True, indent=4)        

      