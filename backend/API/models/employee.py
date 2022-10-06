from datetime import date
import datetime
import time
from models.player import Player

today       = date.today()
now         = str(today)
today       = today.strftime("%B %d, %Y")

today_year  = int(now[:4])
today_month = int(now[5:7])
today_day   = int(now[-2:])

class Employee():

    def __init__(self, id, firstname, lastname, birthdate, connection):
        self.id                 = id
        self.firstname              = firstname
        self.lastname              = lastname
        self.SSN                = birthdate
        self.player             = self.createPlayer(connection)
        self.birthYear          = int(birthdate[:4])
        self.birthMonth         = int(birthdate[4:6])
        self.birthDay           = int(birthdate[-2:])
        self.haveHadBirthday    = False if today_month < self.birthMonth else False if today_month == self.birthMonth and today_day < self.birthDay else True 
        self.age                = today_year - self.birthYear if self.haveHadBirthday else today_year - (self.birthYear+1)
        self.birthDate = date(year=int(birthdate[:4]), month=int(birthdate[4:6]), day=int(birthdate[6:8]))
        self.birthDateText = self.birthDate.strftime("%d %b, %Y")
        self.birthDate = self.birthDate.strftime("%Y-%m-%d")
        self.daysUntilBirthday = (date(year=today_year+1, month=self.birthMonth, day=self.birthDay) - date.today()).days if self.haveHadBirthday else (date(year=today_year, month=self.birthMonth, day=self.birthDay) - date.today()).days

    def getSQLData(self):
        return (self.id, self.firstname, self.lastname, self.SSN)

    def createPlayer(self,connection):
        playerID        = Player.getLatestPlayerId(connection) + 1
        displayName     = f"{self.firstname.capitalize()} {self.lastname.capitalize()[0]}"
        ranking         = 1
        level           = 1
        xp_total        = 0
        xp_month        = 0
        last_login      = date.today().strftime("%Y-%m-%d")
        consecutive_days=0
        birthday_today  = False

        return Player(playerID, self.id, ranking, level,xp_total, xp_month,  last_login, consecutive_days, displayName, birthday_today)
    