import pymysql

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
        getAllDataFromUser(connection, "peter", "stegeby")
        cursor.execute(sql)
        result  = cursor.fetchall()
        printInfo("All the users in this database:", result)
   

    except pymysql.Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        cursor.close()
        connection.close()
        print("\nMySQL connection is closed")


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


def getAllDataFromUser(connection, fname, lname):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM Employee WHERE fname=%s AND lname=%s"
        cursor.execute(sql, (fname, lname))
        result = cursor.fetchone()
        #Will want to have a specific print function for this!
        printRowFormatted(result)

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

main()
