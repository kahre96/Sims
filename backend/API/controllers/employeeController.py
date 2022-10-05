from flask import request
import sys
sys.path.append("../models")
from models.employee import Employee

#TODO: Check if employee with the same emp_ID already exists before adding

class EmployeeController(): 

    def createEmployee(self,mysql):

        # Creating a connection cursor to the database
        cursor = mysql.connection.cursor()
        # Get Parameters from the Request 
        args = request.args
        firstname = args.get("firstname", default="NULL", type=str)
        lastname = args.get("lastname", default="NULL", type=str)
        birthdate = args.get("birthdate", default ="NULL", type=str)
        id=args.get("id", default = "NULL", type=int)

        # Post: Create Employee based on First- and Lastname, birthdate and ID
        if request.method == 'POST':
            
            '''Implementing checks for number of arguments and correct date formatting'''

            if "NULL" in (firstname, lastname, birthdate, id):
                return "Not enough arguments!", 400
            if len(birthdate) != 8:
                return "Sorry! Wrong format, please try with 4 digits of year, 2 digits for month, and 2 digits for day like YYYYMMDD, no spaces and no dashes.", 400
            
            input_year  = int(birthdate[:4])
            input_month = int(birthdate[4:6])
            input_day   = int(birthdate[-2:])

            if input_month > 12 or input_month < 0:
                return ("Month {} is not an option! Please enter a month between 01 - 12".format(input_month)),400
            elif input_month == 2 and input_day > 29:
                return ("February only has 28 sometimes 29 days, please enter a lower value!"), 400
            elif (input_month % 2 == 0 and input_month < 7 or input_month % 2 == 1 and input_month > 8) and input_day > 30:
                return ("Sorry February, April, June, September, and November does not have {} days, 30 is maximum".format(input_day)),400
            
            user = Employee(id, firstname.lower(), lastname.lower(), birthdate, mysql.connection)

            # Adding Employee into DB
            sql     = "INSERT INTO Employee(emp_ID, firstname, lastname, birthdate) VALUES (%s, %s, %s, %s)"
            values  = user.getSQLData()      
            cursor.execute(sql, values)
            # Adding Player into DB
            sql     = "INSERT INTO Player(player_ID, emp_ID, ranking_ID, level,xp_total, xp_month, last_login, consecutive_days) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"
            values  = user.player.getSQLData()
            cursor.execute(sql,values)
 
        #Saving the changes made by the cursor
        mysql.connection.commit()

        #Closing the cursor
        cursor.close()
    
        return ("User " + firstname + " with ID " + str(id) + " was successfully created!"), 201 # Return Name and 201, created

    
employeecontroller = EmployeeController()            