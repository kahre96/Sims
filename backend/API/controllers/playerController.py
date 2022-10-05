from flask import request
from datetime import date, timedelta
import json
import sys
sys.path.append("../models")
from models.player import Player


def getPlayerByID(connection,emp_ID):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT * FROM Player WHERE emp_ID = %s ''' % emp_ID)
            player = cursor.fetchone()
            cursor.execute('''SELECT firstname,lastname FROM Employee WHERE emp_ID = %s ''' % emp_ID)
            name = cursor.fetchone()
            display_name = f"{name[0].capitalize()} {name[1].capitalize()[0]}"
        return Player(player[0],player[1],player[2],player[3],player[4],player[5],player[6], display_name) 

def getPlayerBirthdayByID(connection,emp_ID):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT birthdate FROM Employee WHERE emp_ID = %s ''' % emp_ID)
            employee = cursor.fetchone()
        return employee[0].strftime("%Y%m%d")

class PlayerController():

    def dailyLogin(self, mysql):
        
        xp_to_add = 10 # Standard is 10 XP for a daily login
        birthday_today = False 
        
        today = date.today()
        # Get last weekday in YYYYMMDD Format
        _offsets = (3, 1, 1, 1, 1, 1, 2) 
        last_weekday = (today-timedelta(days=_offsets[today.weekday()]))

        cursor = mysql.connection.cursor()
        args = request.args
        emp_ID = args.get("emp_ID", default="NULL", type=int)
        # Get information on requested player by their emp_ID
        player = getPlayerByID(mysql.connection,emp_ID)

        if id == "NULL":
            return "Request failed, no Employee ID provided!", 400
        else:
            if getPlayerBirthdayByID(mysql.connection,emp_ID)[4:]==today.strftime("%Y%m%d")[4:]:
                xp_to_add += 20
                birthday_today=True
            if player.last_login==last_weekday:
                if player.consecutive_days==4:
                    xp_to_add += 20
                    cursor.execute("UPDATE Player SET consecutive_days = 0 WHERE emp_ID = %s" % emp_ID) 
                else:
                    if player.consecutive_days==2:
                        xp_to_add += 10   
                    cursor.execute("UPDATE Player SET consecutive_days = %s WHERE emp_ID = %s" % (player.consecutive_days+1,emp_ID))
            else:
                cursor.execute("UPDATE Player SET consecutive_days = 0 WHERE emp_ID = %s" % emp_ID) 

            cursor.execute("UPDATE Player SET last_login = %s WHERE emp_ID = %s" % (today.strftime("%Y%m%d"),emp_ID))
            cursor.execute("UPDATE Player SET xp_Total = xp_Total + %s WHERE emp_ID = %s" % (xp_to_add,emp_ID))
        
        #Saving the changes made by the cursor
        mysql.connection.commit()

        #Closing the cursor
        cursor.close()
    
        return getPlayerByID(mysql.connection,emp_ID).toJSON() + "\n \"birthday_today\": " +str(birthday_today), 200



    def test(self, mysql):
         # Creating a connection cursor to the database
        cursor = mysql.connection.cursor()
        # Get Parameters from the Request 
        args = request.args
        emp_ID = args.get("emp_ID", default="NULL", type=int)
        return getPlayerByID(mysql.connection,emp_ID)
            

playercontroller = PlayerController()





