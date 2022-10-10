#from backend.API.app import dailyLogin
from models.player import Player
from flask import request
from datetime import date, timedelta, datetime
import sys
sys.path.append("../models")

# TODO:
# - Add Level functionality
# - Add Rank functionality 
# - Improve getRecent functionality (?)

def getPlayerByID(cursor, emp_ID, birthday_today):
        
        cursor.execute(
            '''SELECT * FROM Player WHERE emp_ID = %s ''' % emp_ID)
        player = cursor.fetchone()
        cursor.execute(
            '''SELECT firstname,lastname FROM Employee WHERE emp_ID = %s ''' % emp_ID)
        name = cursor.fetchone()
        display_name = f"{name[0].capitalize()} {name[1].capitalize()[0]}"
        return Player(player[0], player[1], player[2], player[3], player[4], player[5], player[6], player[7], display_name, birthday_today)

def getPlayerBirthdayByID(cursor, emp_ID):
    
        cursor.execute(
            '''SELECT birthdate FROM Employee WHERE emp_ID = %s ''' % emp_ID)
        employee = cursor.fetchone()
        return employee[0].strftime("%Y%m%d")

class PlayerController():

    def __init__(self):
        self.newEntries = {}
        #self.xp_per_level = 50

    ''' Daily Login function to update player and heroes + return the updated player
    INPUT:  mysql connection and Employee ID
    OUTPUT: Updated Player in JSON Format
    '''
    def dailyLogin(self, mysql, emp_ID):

        # DEFAULT: 10XP, BIRTHDAY = FALSE
        xp_to_add = 10  
        birthday_today = False

        ##############################################################################################
        # GET DATES (TODAY AND LAST WEEKDAY)
        #
        today = date.today()
        _offsets = (3, 1, 1, 1, 1, 1, 2)
        last_weekday = (today-timedelta(days=_offsets[today.weekday()]))
        cursor = mysql.connection.cursor()
        #args = request.args
        #emp_ID = args.get("emp_ID", default="NULL", type=int)

        ##############################################################################################
        # CHECK IF EMP_ID IS PASSED AND VALID
        #  
        if emp_ID == "NULL":
            return "Request failed, no Employee ID provided!", 400
        cursor.execute("select * from Player where emp_ID = %s" % emp_ID)
        data = cursor.fetchall()
        if not data:
            return "Player not found!", 404

        ##############################################################################################
        # CHECK CURRENT LAST LOGIN, BIRTHDAY (Y/N) AND CONSECUTIVE DAYS
        #
        player = getPlayerByID(cursor, emp_ID, birthday_today)
        if player.last_login==today: # return the current stats, don't add XP when played already logged in today
            return player.toJSON(), 200

        if getPlayerBirthdayByID(cursor, emp_ID)[4:] == today.strftime("%Y%m%d")[4:]:
            xp_to_add += 20 # When it's the players birthday: add 20XP and save birthday_today to add to the return object
            birthday_today = True
    
        if player.last_login==last_weekday: # Only increment consecutive days if the last login was on the last weekday 
            if player.consecutive_days==4:
                xp_to_add += 20
            
            if player.consecutive_days==2:
                xp_to_add += 10  

            if player.consecutive_days==5: # Reset counter when player logged in for 5 days in a row
                cursor.execute("UPDATE Player SET consecutive_days = 0 WHERE emp_ID = %s" % emp_ID) 
            else:
                cursor.execute("UPDATE Player SET consecutive_days = %s WHERE emp_ID = %s" % (player.consecutive_days+1,emp_ID))
        
        else: # Reset counter if the last login wasn't on the last weekday
            cursor.execute("UPDATE Player SET consecutive_days = 0 WHERE emp_ID = %s" % emp_ID) 
        
        ##############################################################################################
        # UPDATE XP (PER MONTH AND IN TOTAL)
        #
        if player.last_login.strftime("%Y%m%d")[:6] == today.strftime("%Y%m%d")[:6]: #Check if the most recent XP were gained this month (Has the player logged in this month?)
            cursor.execute("UPDATE Player SET xp_Month = xp_Month + %s WHERE emp_ID = %s" % (xp_to_add,emp_ID)) # Update Monthly XP
        else:
            cursor.execute("UPDATE Player SET xp_Month = 0 + %s WHERE emp_ID = %s" % (xp_to_add,emp_ID)) # Update Monthly XP, when player hasn't logged in this month yet

        cursor.execute("UPDATE Player SET last_login = %s WHERE emp_ID = %s" % (today.strftime("%Y%m%d"),emp_ID)) # Update last login
        cursor.execute("UPDATE Player SET xp_Total = xp_Total + %s WHERE emp_ID = %s" % (xp_to_add,emp_ID)) # Update Total XP

        updated_player = getPlayerByID(cursor,emp_ID,birthday_today) # Get updated Player
        
        ##############################################################################################
        # UPDATE HERO TABLE
        #
        hero_date = updated_player.last_login.strftime("%Y%m%d")
        hero_xp = updated_player.xpMonth
        
        cursor.execute("SELECT * FROM Hero WHERE MONTH(Date)=%s AND YEAR(Date)=%s AND Xp_Month > %s" % (hero_date[4:6],hero_date[:4],hero_xp-1))
        results = cursor.fetchall() # Get all Heroes for current month (That have more XP than current user)
        if len(results) <= 2: # If there's two or less, insert current user regardless of XP. If current user is the third hero, delete the hero with least XP so its still 3 in total
            cursor.execute("INSERT INTO Hero(Emp_ID,Date,Xp_Month) VALUES (%s,%s,%s)" % (emp_ID,hero_date,hero_xp))
            if len(results) == 2:
                cursor.execute("DELETE FROM Hero WHERE MONTH(Date)=%s AND YEAR(Date)=%s ORDER BY XP_Month ASC LIMIT 1 " % (hero_date[4:6],hero_date[:4]))

        ##############################################################################################
        # SAVE CHANGES AND RETURN PLAYER AS JSON
        #
        mysql.connection.commit()
        cursor.close()
        return updated_player.toJSON() # Return Updated stats in JSON format


    ''' New Entry Function used by the AI to push recognized Employees into an array
    INPUT:  mysql connection, Employee ID
    OUTPUT: Dict. of ID/Timestamp
    '''
    def newEntry(self, mysql):
        
        args        = request.args
        emp_ID      = args.get("emp_ID", default="NULL", type=str) 
        timestamp   = 0
        if emp_ID == "NULL":
            return "Request failed, no Employee ID provided!", 400
       
        with mysql.connection.cursor() as cursor:
            sql = """
            SELECT p.player_id, CONCAT(firstname," ",lastname), r.name, p.xp_total, xp_month FROM employee e, player p, ranking r
            WHERE e.emp_ID=%s AND (p.emp_ID = e.emp_ID) AND (p.ranking_id = r.ranking_id)"""
            cursor.execute(sql, emp_ID)
            result      = cursor.fetchone()
            if not result:
                return "Player not found!", 404

            dt          = datetime.now()
            timestamp   = dt.strftime("%H:%M:%S")
            #print(timestamp)
            #player_id, display_name, ranking, xp_total, xp_month = result[0], result[1], result[2], result[3], result[4]
            self.newEntries[emp_ID] = timestamp

            #for key, value in self.newEntries.items():
                #print(key, ":" , value)

            cursor.close()
            #return {"emp_ID":emp_ID, "player_id":player_id, "name":display_name, "rank":ranking, "total_xp":xp_total, "month_xp":xp_month}, 200
            return self.newEntries, 200

    ''' Get all recently recognized players
    INPUT: Mysql connection (also uses the playercontrollers newEntries Dictionary)
    OUTPUT: List of JSON Data for all recently logged in players
    '''
    def getRecent(self,mysql):
        
        employees = []
        for key in self.newEntries.items():
            employees.append(key[1]) # Append the entry-timestemp to the list
            employees.append(self.dailyLogin(mysql,int(key[0]))) # Log in all players and append their JSON Data 

        self.newEntries.clear() # Clear the Dictionary, which is temporarily storing the recently recognized players
        
        if len(employees) == 0:
            return "No new entries!", 400
        
        # Must remake this as a tuple ^^' [22-10-10] Peter
        return employees, 200


playercontroller = PlayerController()





