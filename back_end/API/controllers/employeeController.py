from flask import Flask, render_template, redirect, url_for, request

class EmployeeController(): 

    def createEmployee(self,mysql):
        # Creating a connection cursor to the database
        cursor = mysql.connection.cursor()
        # Get Parameters from the Request 
        args = request.args
        firstname = args.get("firstname", default="", type=str)
        lastname = args.get("lastname", default="", type=str)
        id=args.get("id", default = "", type=str)
        # Post: Create User based on First- and Lastname, ID is Autoincremented
        if request.method == 'POST':
    
            cursor.execute(''' INSERT INTO Employee(fname, lname) VALUES(%s,%s)''',(firstname,lastname))
            case=0
        # Get: Get First- and Lastname by ID
        if request.method == 'GET':
            
            cursor.execute(''' SELECT fname, lname FROM Employee WHERE empid = %s ''' % id)
            records = cursor.fetchall()
            case=1
        
        #Saving the changes made by the cursor
        mysql.connection.commit()

        #Closing the cursor
        cursor.close()

        if case == 0:
            return firstname, 201 # Return Name and 201, created

        elif case == 1:
            return {"Employee:":records} # Return First- and Lastname


employeecontroller = EmployeeController()            