from flask import request, render_template

class AdminController():
        
    def adminPage(self,mysql):
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' or request.form['password'] != 'admin': # Check user input against hard-coded password
                error = 'Invalid Credentials. Please try again.'
            else:
                cursor = mysql.connection.cursor()
                playercount = cursor.execute('SELECT * FROM employee ') # Get total amount of employees (To be changed to players?)
                mysql.connection.commit()
                cursor.close()
                return render_template('statistics.html', data=playercount) # Return Statistics page after sucessfull login
        return render_template('adminForm.html', error=error)

# Create Admin Controller instance to use its functions
admincontroller = AdminController()       