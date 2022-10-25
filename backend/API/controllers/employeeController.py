from flask import request
import sys
from os import listdir, rename
sys.path.append("../models")
from models.employee import Employee

#TODO: Check if employee with the same emp_ID already exists before adding

class EmployeeController(): 

    def createEmployee(self,mysql):

        # Creating a connection cursor to the database
        cursor = mysql.connection.cursor()
        # Get Parameters from the Request 
        args        = request.args
        firstname   = args.get("firstname", default="NULL", type=str)
        lastname    = args.get("lastname", default="NULL", type=str)
        birthdate   = args.get("birthdate", default ="NULL", type=str)
        character   = args.get("character", default ="NULL", type=str)

        # Post: Create Employee based on First- and Lastname, birthdate and ID
        if request.method == 'POST':
            
            '''Implementing checks for number of arguments and correct date formatting'''

            if "NULL" in (firstname, lastname, birthdate):
                return "Not enough arguments!", 400
            
            self.addUser(mysql, firstname, lastname, birthdate)
            sql     = "SELECT emp_id FROM employee WHERE firstname=%s and lastname=%s"
            values  = (firstname.lower(), lastname.lower())
            cursor.execute(sql, values)
            
            # Fetching the id from the newly created employee
            result  = cursor.fetchall()
            emp_id  = result[-1][0]

            user    = Employee(emp_id, firstname.lower(), lastname.lower(), birthdate)
            
            # Adding Player into DB
            sql     = "INSERT INTO Player(emp_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (%s, %s, %s, %s, %s, %s)"
            values  = user.player.getSQLData()
            cursor.execute(sql,values)

            path_run        = "static/characters/running_avatar/"
            path_idle       = "static/characters/idle_avatar/"
            running_avatars = listdir(path_run)
            idle_avatars    = listdir(path_idle)
            for i, filename in enumerate(running_avatars):
                if filename == character:
                    print("Image:", path_run+filename," was renamed to => ", path_run+"emp_"+str(emp_id)+".gif")
                    rename(path_run+filename, path_run+"emp_"+str(emp_id)+".gif")
            
            for i, filename in enumerate(idle_avatars):
                if filename == character:
                    print("Image:", path_idle+filename," was renamed to => ", path_idle+"emp_"+str(emp_id)+".gif")
                    rename(path_idle+filename, path_idle+"emp_"+str(emp_id)+".gif")
            #Closing the cursor
            cursor.close()   

        #Saving the changes made by the cursor
        mysql.connection.commit()

        return ("User " + firstname + " with ID " + str(id) + " was successfully created!"), 201 # Return Name and 201, created

    def addUser(self, mysql, firstname, lastname, birthdate):
        with mysql.connection.cursor() as cursor:
            values = (firstname.lower(), lastname.lower(), birthdate)

            # Adding Employee into DB
            sql     = "INSERT INTO Employee(firstname, lastname, birthdate) VALUES (%s, %s, %s)"
            cursor.execute(sql, values)
        mysql.connection.commit()
    
employeecontroller = EmployeeController()            