import pymysql
from datetime import date
import datetime
import time

today       = date.today()
now         = str(today)
today       = today.strftime("%B %d, %Y")

today_year  = int(now[:4])
today_month = int(now[5:7])
today_day   = int(now[-2:])


XP_PER_LEVEL = 50
DICT_WITH_QUERIES = {}
NEXT_INDEX_PLAYER_ID = 0

# *** Ways to gain xp ***
# Coming in
# Close to when they start
# 3 consecutive days of the week
# Double xp on birthdays
# First one to reach maximum value gets first spot (?)

# Display 3 top players with names and the rest with just avatars and colours
# ATTRIBUTE FOR PLAYERS xp_this_month

# Random RGB colours

def main():
    connection = pymysql.connect(host="localhost",
                             user="root",
                             password="27amc81pqt01pab52mnc",
                             database="emp_info")

    try:
        cursor  = connection.cursor()
        cursor.execute("SELECT database();")
        db      = formatTupleIntoStr(cursor.fetchone())
        print("Today: {}\n".format(today))
        print("You are connected to database: ", db)
        table   = "`Employee`"
        query   = "*"
        sql     = "SELECT {} FROM {};".format(query, table)
        #addUser(connection)
        #updateUser(connection)
        fillDBWithDatesOfTheWeek(connection)
        #getInfo(connection)
        #getAllDataFromUser(connection, "peter", "stegeby")
        cursor.execute(sql)
        result  = cursor.fetchall()
        #writeOwnQuery(connection)
        global DICT_WITH_QUERIES
        DICT_WITH_QUERIES   = dictWithXMostQueries(connection, 2)
        for tuple in result:
            #getAllDataFromUser(connection, tuple[1], tuple[2])
            print()
        #printInfo("All the users in this database:", result)
   

    except pymysql.Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        cursor.close()
        connection.close()
        print("\nMySQL connection is closed")

# I will need to ask knowit how their EmpId is formatted to know if I should use string or int.
def addUser(connection):
    with connection.cursor() as cursor:
        print("\nAdding a new user to the database:")
        #Fetch how many current users there are in the database
        currentUsers = cursor.execute("SELECT * FROM Employee")
        #Adding one to how many users as a new ID for the new user in the database
        newId   = currentUsers+1
        fname   = input("Please enter firstname: >")
        lname   = input("Please enter  lastname: >")
        while (True):
            bdate       = input("Please enter birthdate: (YYYYMMDD) >")
            input_year  = int(bdate[:4])
            input_month = int(bdate[4:6])
            input_day   = int(bdate[-2:])
            if len(bdate) != 8:
                print("Sorry! Wrong format, please try with 4 digits of year, 2 digits for month, and 2 digits for day like YYYYMMDD, no spaces and no dashes.")
            elif input_year < (today_year-100):
                choice = input("Are you sure you are older than a 100 years old? (Y/N) >")
                if choice.upper() == "Y":
                    print("My bad, your age seemed suspicious! Welcome to the database {} {}".format(fname, lname))
                    break;
            elif input_month > 12 or input_month < 0:
                print("Month {} is not an option! Please enter a month between 01 - 12".format(input_month))
            elif input_month == 2 and input_day > 29:
                print("February only has 28 sometimes 29 days, please enter a lower value! =)")
            elif (input_month % 2 == 0 and input_month < 7 or input_month % 2 == 1 and input_month > 8) and input_day > 30:
                print("Sorry February, April, June, September, and November does not have {} days, 30 is maximum".format(input_day))
            else:
                print("Everything looks good! Welcome {} {} with birhdate {}!".format(fname, lname, bdate))
                choice = input("Does everything look good? (Y/N) >")
                if choice.upper() == "Y":
                    print("I am happy that you are pleased, have a good day!")
                    break;
        global NEXT_INDEX_PLAYER_ID 
        NEXT_INDEX_PLAYER_ID = getLatestPlayerId(connection) + 1
        user    = Employee(newId, fname.lower(), lname.lower(), bdate)
        # Adding Employee into DB
        sql     = "INSERT INTO Employee(emp_id, Fname, Lname, Birthdate) VALUES (%s, %s, %s, %s)"
        values  = user.getSQLData()      
        cursor.execute(sql, values)
        # Adding Player into DB
        sql     = "INSERT INTO Player(player_id, emp_id, ranking_tier, xp_total, xp_month, level) VALUES (%s, %s, %s, %s, %s, %s)"
        values  = user.player.getSQLData()
        cursor.execute(sql,values)
        # Adding Requirement for xp_next_level into DB
        sql     = "INSERT INTO Player_Meets_Requirement(Player_id, Requirement_id, Value) VALUES (%s, %s, %s)"
        values  = (user.player.playerId, 1, 50)
        cursor.execute(sql,values)
    #Making the changes unto the database
    connection.commit()

def updateUser(connection):
    with connection.cursor() as cursor:
        emp_id = input("Enter an emp_id >")
        cursor.execute(f"SELECT fname, lname, player_id, xp_total, level FROM employee e, player p WHERE e.emp_id = p.emp_id AND e.emp_id = {emp_id}")
        temp = cursor.fetchone()
        fname, lname, player_id, current_xp, current_level = temp[0].capitalize(), temp[1].capitalize(), temp[2], int(temp[3]), int(temp[4])
        print(f"User chosen is ({fname} {lname} with player_id {player_id})")
        xp_total = input("Enter new total xp (Current xp: {}) >".format(current_xp))
        diff = xp_total - current_xp
        sql = f"""
        UPDATE Player
        SET xp_total = {xp_total}
        WHERE emp_id = {emp_id}"""
        cursor.execute(sql)
        select = "SELECT pmr.Value, req.value FROM Player_Meets_Requirement pmr, player p, requirement req WHERE req.id = 1 AND pmr.player_id = p.player_id AND req.id = pmr.requirement_id"
        cursor.execute(select)
        temp = cursor.fetchone()
        current_xp_needed, xp_per_level = int(temp[0]), int(temp[1])
        select = "SELECT value, tier FROM requirement AS req, ranking r WHERE req.name = r.name"
        cursor.execute(select)
        temp = cursor.fetchone()
        ranking_req, current_tier           = int(temp[0]), int(temp[1])
        xp_next_level                       = xp_per_level * ranking_req * current_level
        new_xp_next_level                   = xp_next_level - int(xp_total)
        new_xp_needed                       = current_xp_needed - diff
        print("new_xp_needed: ", new_xp_needed)
        # Would like to have a system so that level jumps to the correct value right away using modulus instead of having to iterate [22-09-27]
        if new_xp_needed <= 0:
            new_level = current_level + 1
            while new_xp_next_level < 0:
                new_level += 1
                new_xp_next_level = (xp_per_level * ranking_req * new_level) - int(xp_total)
                print("Level: ", new_level)
                print("new_xp_next_level: ", new_xp_next_level)
        sql = f"""
        UPDATE Player
        SET level = {new_level}
        WHERE emp_id = {emp_id}"""
        cursor.execute(sql)
        sql = f"""
        UPDATE Player_meets_requirement pmr
        INNER JOIN Player p
        ON pmr.player_id = p.player_id
        SET 
        value = {new_xp_next_level}
        WHERE p.player_id = {player_id}"""
        cursor.execute(sql)
        
    connection.commit()

def getInfo(connection):
    with connection.cursor() as cursor:
        cursor.execute("SHOW tables;")
        tables = cursor.fetchall()
        printInfo("A List of all the tables:", tables)
        choice = input("Which database would you like to see? >")
        cursor.execute("DESCRIBE {}".format(choice))
        rows = cursor.fetchall()
        printInfo("A Decription of the table:", rows)

def writeOwnQuery(connection):
    with connection.cursor() as cursor:
        query = input("What do you want to search for? >")
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        for tuple in result:
            getAllDataFromUser(connection, tuple[1], tuple[2])
            print()

def getAllDataFromUser(connection, fname, lname):
    """Good for creating a player, but this function is just for the developer, will not be used for front-end purposes!"""
    with connection.cursor() as cursor:
        id = "SELECT emp_ID FROM Employee WHERE fname=%s AND lname=%s"
        cursor.execute(id, (fname, lname))
        result = cursor.fetchone()
        #Will want to have a specific print function for this!
        
        result = formatTupleIntoStr(result)
        sql = "SELECT * FROM Employee AS e, Player AS p, Ranking AS r WHERE (e.emp_ID=%s AND p.emp_ID=%s) AND p.ranking_tier = r.tier"
        cursor.execute(sql, (result, result))
        result = cursor.fetchone()
        temp = list(result)
        #Storing values of temp to named variables to increase readability
        empID, tier, displayName, playerID, xp = str(temp[0]), temp[11], f"{temp[1].capitalize()} {temp[2].capitalize()[0]}", str(temp[5]), temp[7]
        xp_month, level = temp[8], temp[9]
        player = Player(empID, playerID, tier, displayName, xp, xp_month, level)
        player.print()

def printInfo(str, arr):
    rowpadder   = "*"
    length      = 50
    print("\n",str)
    print(rowpadder * length)
    for row in arr:
        printRowFormatted(row)
    print(rowpadder * length)

def printRowFormatted(tup):
    arr         = list(tup)
    userId      = arr[0]
    fname       = arr[1].capitalize()
    lname       = arr[2].capitalize()
    birthdate   = str(arr[3]).replace('-','')
    emp         = Employee(userId, fname, lname, birthdate)
    emp.print()

def printPlayerFromList(list):
    space = " "
    title_list = ["EmpID", "PlayerID", "Rank", "Name", "Experience", "Level"]
    length = len(list[3]) if len(list[3]) > 10 else 10
    padding = space * 7
    padding2 = space*length
    str = f'{title_list[0]}{padding}{title_list[1]}{padding}{title_list[2]}{padding}{title_list[3]}{padding}{title_list[4]}{padding}{title_list[5]}'
    print(str)
    result = ""
    for i in range(len(list)):
        if (i < len(list)):
            padding2 = space*(len(title_list[i]) + 7 - len(str(list[i])))
            if i == len(list)-1:
                result += f'{list[i]}'
            else:
                result += f'{list[i]}{padding2}'
    
    print(result)

def dictWithXMostQueries(connection, x):
    with connection.cursor() as cursor:
        temp_dict = {}

        sql = "SELECT * FROM query ORDER BY times_used DESC"
        cursor.execute(sql)
        result = cursor.fetchall()
        index = 0
        for tuple in result:
            temp_dict[tuple[0]] = tuple[1]
            index+=1
            if index == x:
                break

        return temp_dict

#Format the id from (digit, ) to digit
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
    def print(self):
        printPlayerFromList([str(self.empId), str(self.playerId), self.rank, self.displayName, str(self.xpTotal), str(self.level)])
    def getSQLData(self):
        return (self.playerId ,self.empId, self.rank, self.xpTotal, self.xpMonth, self.level)

# Fix so that the longest first- and lastname are stored so that all lines are formatted in the same way (Later fix!) 22-09-22
class Employee():
    """An employee where arguments in __init__ is the same order as in the db and some members are used to calculate age and such!"""
    def __init__(self, id, fname, lname, birthdate):
        self.id                 = id
        self.fname              = fname
        self.lname              = lname
        self.SSN                = birthdate
        self.player             = self.createPlayer()
        self.birthYear          = int(birthdate[:4])
        self.birthMonth         = int(birthdate[4:6])
        self.birthDay           = int(birthdate[-2:])
        self.haveHadBirthday    = False if today_month < self.birthMonth else False if today_month == self.birthMonth and today_day < self.birthDay else True 
        self.age                = today_year - self.birthYear if self.haveHadBirthday else today_year - (self.birthYear+1)
        self.birthDate = date(year=int(birthdate[:4]), month=int(birthdate[4:6]), day=int(birthdate[6:8]))
        self.birthDateText = self.birthDate.strftime("%d %b, %Y")
        self.birthDate = self.birthDate.strftime("%Y-%m-%d")
        self.daysUntilBirthday = (date(year=today_year+1, month=self.birthMonth, day=self.birthDay) - date.today()).days if self.haveHadBirthday else (date(year=today_year, month=self.birthMonth, day=self.birthDay) - date.today()).days
    def print(self):
        fname = self.fname.capitalize()
        lname = self.lname.capitalize()
        space       = ' '
        length      = 8-len(self.fname)
        padding     = space*length
        length      = 12-len(self.lname)
        padding2    = space*length
        print(f"{self.id}: {space*(3-len(str(self.id)))}{fname}{padding}{lname}{padding2}{self.birthDate}{space*4}{self.age} years old")

    def getSQLData(self):
        return (self.id, self.fname, self.lname, self.SSN)

    def createPlayer(self):
        playerID        = NEXT_INDEX_PLAYER_ID
        displayName     = f"{self.fname.capitalize()} {self.lname.capitalize()[0]}"
        ranking         = 1
        xp_total        = 0
        xp_month        = 0
        level           = 1
        xp_next_level   = 50
        return Player(playerID, self.id, ranking, displayName, xp_total, xp_month, level)


def getLatestPlayerId(connection):
    with connection.cursor() as cursor:
        sql = "SELECT Player_ID FROM Player ORDER BY Player_ID DESC LIMIT 1";
        cursor.execute(sql)
        result = formatTupleIntoStr(cursor.fetchone())
        return int(result)

    # https://stackoverflow.com/questions/56163008/how-to-get-all-dates-of-week-based-on-week-number-in-python
def fillDBWithDatesOfTheWeek(connection):
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE Day CASCADE;")
        create = """
        CREATE TABLE Day (
        Date    DATE NOT NULL,
        PRIMARY KEY(Date));
        """
        cursor.execute(create)
        theday = datetime.date.today()
        weekday = theday.isoweekday()
        # The start of the week
        start = theday - datetime.timedelta(days=(weekday-1))
        # build a simple range
        dates = [start + datetime.timedelta(days=d) for d in range(5)]
        dates = [str(d).replace('-','') for d in dates]
        for date in dates:
            sql = "INSERT INTO Day(date) VALUES(%s)"
            cursor.execute(sql, date)
    connection.commit()

main()
