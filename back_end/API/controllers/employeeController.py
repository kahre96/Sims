from flask import Flask, render_template, redirect, url_for, request
import sys, os
sys.path.append("../models")
from models.employee import Employee

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

            case=0

        # Get: Get First- and Lastname by ID
        if request.method == 'GET':
            
            cursor.execute(''' SELECT fname, lname FROM Employee WHERE Emp_id = %s ''' % id)
            records = cursor.fetchall()
            case=1
        
        #Saving the changes made by the cursor
        mysql.connection.commit()

        #Closing the cursor
        cursor.close()

        if case == 0:
            return ("User " + firstname + " with ID " + str(id) + " was successfully created!"), 201 # Return Name and 201, created

        elif case == 1:
            return {"Employee:":records} # Return First- and Lastname


employeecontroller = EmployeeController()            