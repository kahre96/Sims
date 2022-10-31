from turtle import update
from models.player import Player
from flask import request
from datetime import date, timedelta, datetime
import sys
import json
sys.path.append("../models")


''' Helper Function to get Player Object by employee ID and birthday_today variable'''
def getPlayerByID(cursor, emp_ID, birthday_today):
        
        cursor.execute(
            "SELECT * FROM Player WHERE emp_ID = %s " % emp_ID)
        player = cursor.fetchone()
        cursor.execute(
            "SELECT firstname,lastname FROM Employee WHERE emp_ID = %s " % emp_ID)
        name = cursor.fetchone()
        display_name = f"{name[0].capitalize()} {name[1].capitalize()[0]}"
        return Player(player[0], player[1], player[2], player[3], player[4], player[5],display_name, birthday_today)

''' Helper Function to return players birthday '''
def getPlayerBirthdayByID(cursor, emp_ID):
    
        cursor.execute(
            "SELECT birthdate FROM Employee WHERE emp_ID = %s " % emp_ID)
        employee = cursor.fetchone()
        return employee[0].strftime("%Y%m%d")

''' Helper function to select Greeting for the player'''
def greet(cursor, player, first_login):   
        greeting = "Hej"     
        if first_login == True: # Is it the players first login today?
            if player.birthday_today == True: # Player birthday is today: Randomly select from birthday greetings
                cursor.execute("SELECT Text FROM Greeting WHERE Category = 'birthday' ORDER BY RAND() LIMIT 1")
            elif int(datetime.now().strftime("%H")) < 10: # It's before 10AM: Randomly select from default OR morning greetings
                cursor.execute("SELECT Text FROM Greeting WHERE Category = 'default' OR Category = 'morning' ORDER BY RAND() LIMIT 1")
            else: # Randomly select regular greeting
                cursor.execute("SELECT Text FROM Greeting WHERE Category = 'default' ORDER BY RAND() LIMIT 1")
        else: 
            cursor.execute("SELECT Text FROM Greeting WHERE Category = 'second' ORDER BY RAND() LIMIT 1")
    
        greeting = cursor.fetchone() 
        greeting = str(greeting[0]) + "!"
        player.greeting = greeting # Update the players greeting
        return player    

''' Helper function to update the XP needed for the next level, and the XP the player has towards it'''
def setPlayerXPLevel(levels,level, player, xp):
        if xp >= max(levels.values()): # Set xp to next level to 0 if Player has reached the maximum level
            player.xpNextLevel = 0
            player.xpLevel = 0
        else:
            player.xpLevel = player.xpTotal  - levels[level]
            player.xpNextLevel = levels[level+1]-levels[level]
        return player    
                

class PlayerController():

    def __init__(self):
        self.newEntries = {} # Used to keep track of recently recognized players
        self.Levels = { # Defines the XP requirements for the specific levels
            1:  0,
            2:  50,
            3:  100,
            4:  150,    
            5:  200,
            6:  250,
            7:  350,
            8:  450,
            9:  600,
            10: 800,
            11: 1000,
            12: 1300,
            13: 1600,
            14: 2000,
            15: 2400,
            16: 2800,
            17: 3500,
            18: 4200,
            19: 5000,
            20: 6000,
        }
        self.usedMonths = []


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
            player = greet(cursor, player, False)
            player = setPlayerXPLevel(self.Levels, player.level, player, player.xpTotal)
            return player

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

        ##############################################################################################
        # UPDATE LEVEL
        #
        xp = player.xpTotal + xp_to_add # Total XP of updated player (without another DB query)
        level = 1
        
        for key in self.Levels:
            if self.Levels[key] <= xp:
                level = key
        # Update Level in the database
        cursor.execute("UPDATE Player SET Level = %s WHERE emp_ID = %s" % (level,emp_ID))
                    
        ##############################################################################################
        # UPDATE XPLEVEL, XPNEXTLEVEL AND HERO TABLE
        #
        updated_player = getPlayerByID(cursor,emp_ID,birthday_today) # Get updated Player
        updated_player = setPlayerXPLevel(self.Levels,level,updated_player,xp)

        hero_date = updated_player.last_login.strftime("%Y%m%d")
        hero_xp = updated_player.xpMonth
        
        cursor.execute("SELECT * FROM Hero WHERE MONTH(Date)=%s AND YEAR(Date)=%s AND Xp_Month > %s" % (hero_date[4:6],hero_date[:4],hero_xp-1))
        results = cursor.fetchall() # Get all Heroes for current month (That have more XP than current user)
        if len(results) <= 2: # If there's two or less, insert current user regardless of XP
            cursor.execute("SELECT * FROM Hero WHERE Emp_ID = %s AND MONTH(Date)=%s AND YEAR(Date)=%s" % (emp_ID,hero_date[4:6],hero_date[:4]))
            if cursor.fetchone() == None: # Check if player is already in this months heroes 
                cursor.execute("INSERT INTO Hero(Emp_ID,Date,Xp_Month) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE Date = %s, Xp_Month = %s" % (emp_ID,hero_date,hero_xp,hero_date,hero_xp))
            else:
#                 cursor.execute("UPDATE Hero SET Date = %s, Xp_Month = %s WHERE Emp_ID = %s ON DUPLICATE KEY UPDATE Date = %s, Xp_Month = %s" % (hero_date,hero_xp,emp_ID,hero_date,hero_xp))
                cursor.execute("UPDATE Hero SET Date = %s, Xp_Month = %s WHERE Emp_ID = %s" % (hero_date,hero_xp,emp_ID))
            # Check if there are more than 3 Heroes for this month after insertion. If so, delete the one with least XP
            cursor.execute("SELECT * FROM Hero WHERE MONTH(Date)=%s AND YEAR(Date)=%s" % (hero_date[4:6],hero_date[:4]) )
            results = cursor.fetchall()
            if len(results) > 3:
                cursor.execute("DELETE FROM Hero WHERE MONTH(Date)=%s AND YEAR(Date)=%s ORDER BY XP_Month ASC LIMIT 1 " % (hero_date[4:6],hero_date[:4]))

        ##############################################################################################
        # SAVE CHANGES AND RETURN PLAYER AS JSON
        #
        updated_player=greet(cursor, updated_player, True) # Update player greeting
        updated_player.xpGained=xp_to_add
        mysql.connection.commit()
        cursor.close()
        return updated_player # Return Updated stats in JSON format


    ''' New Entry Function used by the AI to push recognized Employees into an array
    INPUT:  mysql connection, Employee ID
    OUTPUT: Dict. of ID/Timestamp
    '''
    def newEntry(self, mysql):
        
        args        = request.args
        emp_ID      = args.get("emp_ID", default="NULL", type=int) 
        timestamp   = 0
        if emp_ID == "NULL":
            return "Request failed, no Employee ID provided!", 400
       
        with mysql.connection.cursor() as cursor:
            if not(emp_ID==0):
                cursor.execute("SELECT * FROM Player WHERE Emp_ID = %s"% emp_ID)
                result      = cursor.fetchone()
                if not result:
                    return "Player not found!", 404

            dt          = datetime.now()
            timestamp   = dt.strftime("%H:%M:%S")
            self.newEntries[emp_ID] = timestamp

            cursor.close()
            return self.newEntries, 200


    ''' Get last months Top Three players (most monthly XP)
    INPUT: Mysql connection 
    OUTPUT: Dictionary of lists with Player Display Name and Employee ID
    '''
    def getTop(self,mysql):
         with mysql.connection.cursor() as cursor:
            # Get last months date by getting the first day of this month and going back one day
            first_day_this_month = (date.today().replace(day=1))   
            last_month = (first_day_this_month-timedelta(days=1)).strftime("%Y%m%d")
            # Select the top players for last month
            cursor.execute("SELECT Emp_ID From Hero WHERE MONTH(Date)=%s AND YEAR(Date)=%s ORDER BY Xp_Month DESC" % (last_month[4:6],last_month[:4]))
            employees = cursor.fetchall()
            top = {}
            # Create Dict, including List of Employee ID and Display Name
            for emp in employees:
                player = getPlayerByID(cursor,emp[0],False)
                top[employees.index(emp)+1]=(player.displayName,player.emp_id)

            return top


    ''' Get all recently recognized players
    INPUT: Mysql connection (also uses the playercontrollers newEntries Dictionary)
    OUTPUT: List of JSON Data for all recently logged in players
    '''
    def getRecent(self,mysql):
        
        employees = []
        for key in self.newEntries.items():
            if key[0]==0:
                employees.append(Player(0,0,0,0,datetime.today(),0,"Guest",False))
            else:    
                employees.append(self.dailyLogin(mysql,int(key[0])))

        self.newEntries.clear() # Clear the Dictionary, which is temporarily storing the recently recognized players
        
        if len(employees) == 0:
            return [],204

        return json.dumps([obj.__dict__ for obj in employees],indent=4, sort_keys=True, default=str,ensure_ascii=False).encode('utf-8'),200


    ''' Get all monthly XP for all players
    INPUT: Mysql connection 
    OUTPUT: Dictionary with all Employee IDs and corresponding XP this month
    '''
    def getMonthlyXP(self,mysql):
        today = date.today()
        now   = str(today)
        print("now: ", now)
        today_day = int(now[-2:])
        if today_day == 1:
            with mysql.connection.cursor() as cursor:
                if len(self.usedMonths) == 12:
                    self.usedMonths.clear
         
                if now not in self.usedMonths:
                    self.usedMonths.append(now)
                    cursor.execute("UPDATE player SET xp_month = %s", ("0",))
                    print("All the users monthly_xp has been set to 0!")
                    mysql.connection.commit()
        
        with mysql.connection.cursor() as cursor:
            monthlyXP = {}
            cursor.execute("SELECT emp_ID,XP_Month FROM Player")
            players = cursor.fetchall()
            for xp in players:
                cursor.execute(
                    "SELECT firstname,lastname FROM Employee WHERE emp_ID = %s " % xp[0])
                name = cursor.fetchone()
                display_name = f"{name[0].capitalize()} {name[1].capitalize()[0]}"
                monthlyXP[xp[0]]=(xp[1],display_name)
            return monthlyXP,200


playercontroller = PlayerController()





