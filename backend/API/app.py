from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from controllers.employeeController import employeecontroller
from controllers.adminController import admincontroller
from controllers.playerController import playercontroller

#db_password = '27amc81pqt01pab52mnc'
#db_name = 'emp_info'
db_password = ''
db_name = 'sims'

# Define App and open connection to the mysql database
app = Flask(__name__)
app.config['MYSQL_HOST']        = 'localhost'
app.config['MYSQL_USER']        = 'root'
app.config['MYSQL_PASSWORD']    = db_password
app.config['MYSQL_DB']          = db_name
mysql = MySQL(app)

# Route to create employees and get their name based on ID
@app.route('/employee/create', methods = ['POST'])
def employee():
    return employeecontroller.createEmployee(mysql)
    
# Route for admin to see statistics     
@app.route('/admin', methods = ['GET','POST'])
def admin():
    return admincontroller.adminPage(mysql)

@app.route('/employee/dailyLogin', methods = ['GET','POST'])
def dailyLogin():
    return playercontroller.dailyLogin(mysql)

@app.route('/employee/newEntry', methods = ['GET', 'POST'])
def newEntries():
    return playercontroller.newEntry(mysql)


app.run(host='localhost', port=5000)
