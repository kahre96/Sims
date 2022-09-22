import pymysql

XP_PER_LEVEL = 50
DICT_WITH_QUERIES = {}

def main():
    connection = pymysql.connect(host="localhost",
                             user="root",
                             password="27amc81pqt01pab52mnc",
                             database="emp_info")

    try:
        cursor  = connection.cursor()
        cursor.execute("SELECT database();")
        db      = cursor.fetchone()
        print("You are connected to database: ", db)
        table = "`Employee`"
        query = "`EmpId`, `Fname`, `Lname`"
        sql   = "SELECT {} FROM {};".format(query, table)
        #addUser(connection, table)
        #getInfo(connection)
        #getAllDataFromUser(connection, "peter", "stegeby")
        cursor.execute(sql)
        result  = cursor.fetchall()
        #writeOwnQuery(connection)
        DICT_WITH_QUERIES = dictWithXMostQueries(connection, 2)
        print(DICT_WITH_QUERIES)
        #for tuple in result:
            #getAllDataFromUser(connection, tuple[1], tuple[2])
            #print()
        #printInfo("All the users in this database:", result)
   

    except pymysql.Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        cursor.close()
        connection.close()
        print("\nMySQL connection is closed")

# I will need to ask knowit how their EmpId is formatted to know if I should use string or int.
def addUser(connection, table):
    with connection.cursor() as cursor:
        print("\nAdding a new user to the database:")
        #Fetch how many current users there are in the database
        currentUsers = cursor.execute("SELECT * FROM {}".format(table))
        #Adding one to how many users as a new ID for the new user in the database
        newId = currentUsers+1
        fname = input("Please enter firstname: >")
        lname = input("Please enter  lastname: >")
        values = (newId, fname, lname)
        sql = "INSERT INTO {} VALUES (%s, %s, %s)".format(table)
        cursor.execute(sql, values)
    #Making the changes unto the database
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
    with connection.cursor() as cursor:
        id = "SELECT empID FROM Employee WHERE fname=%s AND lname=%s"
        cursor.execute(id, (fname, lname))
        result = cursor.fetchone()
        #Will want to have a specific print function for this!
        result = str(result)
        #Format the id from (digit, ) to digit
        for character in ')(,':
            result = result.replace(character, '')
        sql = "SELECT * FROM Employee AS emp, Player AS pl WHERE emp.empID=%s AND pl.empID=%s"
        cursor.execute(sql, (result, result))
        result = cursor.fetchone()
        temp = list(result)
        #Storing values of temp to named variables to increase readability
        empID, fName, lName, playerID, xp = str(temp[0]), temp[1].capitalize(), temp[2].capitalize(), str(temp[3]), temp[5]
        level = xp // XP_PER_LEVEL
        #To decide how much xp is needed take the xp for a level minus the rest of dividing xp with xp_per_level
        xp_till_next_level = XP_PER_LEVEL - (xp % XP_PER_LEVEL)
        result = [empID, playerID, fName, lName, str(xp), str(level), str(xp_till_next_level)]
        printUserFromList(result)

def printInfo(str, arr):
    rowpadder = "*"
    print("\n",str)
    print(rowpadder * 25)
    for row in arr:
        printRowFormatted(row)
    print(rowpadder * 25)

def printRowFormatted(tup):
    space = " "
    arr = list(tup)
    userId= arr[0]
    fname = arr[1].capitalize()
    #Might need to change 8 depening on how long the longest name in the database is ^^'
    ##Could fix that dynamically somehow aswell
    padding = 8-len(fname)
    lname = arr[2].capitalize()
    print("{}: {}{} {}".format(userId,fname,(space*padding),lname))

def printUserFromList(list):
    space = " "
    title_list = ["EmpID", "PlayerID", "Firstname", "Lastname", "Experience", "Level", "Next Level"]
    length = len(list[2]) if len(list[2]) > len(list[3]) else len(list[3])
    length = 10 if length < 10 else length
    padding = space * 3
    padding2 = space*length
    str = f'{title_list[0]}{padding}{title_list[1]}{padding}{title_list[2]}{padding}{title_list[3]}{padding}{title_list[4]}{padding}{title_list[5]}{padding}{title_list[6]}'
    print(str)
    result = ""
    for i in range(len(list)):
        if (i < len(list)):
            padding2 = space*(len(title_list[i]) + 3 - len(list[i]))
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
    

main()
