from models.player import Player
from flask import request
from datetime import date, timedelta
import sys
sys.path.append("../models")

# PETER
# xp_month reset and update


def getPlayerByID(connection, emp_ID, birthday_today):
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT * FROM Player WHERE emp_ID = %s ''' % emp_ID)
            player = cursor.fetchone()
            cursor.execute(
                '''SELECT firstname,lastname FROM Employee WHERE emp_ID = %s ''' % emp_ID)
            name = cursor.fetchone()
            display_name = f"{name[0].capitalize()} {name[1].capitalize()[0]}"
        return Player(player[0], player[1], player[2], player[3], player[4], player[5], player[6], player[7], display_name, birthday_today)


def getPlayerBirthdayByID(connection, emp_ID):
        with connection.cursor() as cursor:
            cursor.execute(
                '''SELECT birthdate FROM Employee WHERE emp_ID = %s ''' % emp_ID)
            employee = cursor.fetchone()
        return employee[0].strftime("%Y%m%d")




class PlayerController():

    def dailyLogin(self, mysql):

        xp_to_add = 10  # Standard is 10 XP for a daily login
        birthday_today = False

        today = date.today()
        # Get last weekday in YYYYMMDD Format
        _offsets = (3, 1, 1, 1, 1, 1, 2)
        last_weekday = (today-timedelta(days=_offsets[today.weekday()]))

        cursor = mysql.connection.cursor()
        args = request.args
        emp_ID = args.get("emp_ID", default="NULL", type=int)

        # Check if existing employee ID was passed
        if id == "NULL":
            return "Request failed, no Employee ID provided!", 400
        cursor.execute("select * from Player where emp_ID = %s" % emp_ID)
        data = cursor.fetchall()
        if not data:
            return "Player not found!", 404

         # Get information on requested player by their emp_ID
        player = getPlayerByID(mysql.connection, emp_ID, birthday_today)
        
        if player.last_login==today: # return the current stats, don't add XP when played already logged in today
            return player.toJSON(), 200

        if getPlayerBirthdayByID(mysql.connection, emp_ID)[4:] == today.strftime("%Y%m%d")[4:]:
            xp_to_add += 20 # When it's the players birthday: add 20XP and save birthday_today to add to the return object
            birthday_today = True
    
        if player.last_login==last_weekday: # Only increment consecutive days if the last login was on the last weekday 
            if player.consecutive_days==4:
                xp_to_add += 20
            
            if player.consecutive_days==2:
                xp_to_add += 10  

            if player.consecutive_days==5:
                cursor.execute("UPDATE Player SET consecutive_days = 0 WHERE emp_ID = %s" % emp_ID) 
            else:
                cursor.execute("UPDATE Player SET consecutive_days = %s WHERE emp_ID = %s" % (player.consecutive_days+1,emp_ID))
        
        else:
            cursor.execute("UPDATE Player SET consecutive_days = 0 WHERE emp_ID = %s" % emp_ID) 

        cursor.execute("UPDATE Player SET last_login = %s WHERE emp_ID = %s" % (today.strftime("%Y%m%d"),emp_ID)) # Update last login
        cursor.execute("UPDATE Player SET xp_Total = xp_Total + %s WHERE emp_ID = %s" % (xp_to_add,emp_ID)) # Update XP
    
        # Saving the changes made by the cursor
        mysql.connection.commit()

        updated_player = getPlayerByID(mysql.connection,emp_ID,birthday_today)

        cursor.close()

        return updated_player.toJSON(), 200 # Return Updated stats in JSON format

playercontroller = PlayerController()





