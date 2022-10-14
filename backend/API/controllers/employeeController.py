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
            emp_id  = int(cursor.fetchone()[0])

            user    = Employee(emp_id, firstname.lower(), lastname.lower(), birthdate)
            
            # Adding Player into DB
            sql     = "INSERT INTO Player(emp_ID, ranking_ID, level, xp_total, xp_month, last_login, consecutive_days) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values  = user.player.getSQLData()
            cursor.execute(sql,values)

            #self.addCharacter(mysql, character, emp_id)

            path = "static/characters/" 
            images_in_dir = listdir(path)
            for i, filename in enumerate(images_in_dir):
                if i == int(character):
                    print("Image:", path+filename," was renamed to => ", path+"zzz_"+str(emp_id)+".gif")
                    rename(path+filename, path+"zzz_"+str(emp_id)+".gif")
            
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

    # Should probably be able to remove this We´re not going to store character in database! [22-10-14]
    def addCharacter(self, mysql, character_id, emp_id):
        with mysql.connection.cursor() as cursor:
            values  = (character_id, emp_id)

            # Adding Character into DB
            sql     = "INSERT INTO Char_emp(char_id, emp_id) VALUES (%s, %s)"
            cursor.execute(sql, values)
        mysql.connection.commit()
    
employeecontroller = EmployeeController()            