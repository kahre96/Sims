from flask import Flask, render_template, redirect, url_for, request
from flask_mysqldb import MySQL
from controllers.employeeController import employeecontroller
from controllers.adminController import admincontroller
from controllers.playerController import playercontroller

# Define App and open connection to the mysql database
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sims'
mysql = MySQL(app)

# Route to create employees and get their name based on ID
@app.route('/employee', methods = ['POST','GET'])
def employee():
    return employeecontroller.createEmployee(mysql)
    
# Route for admin to see statistics     
@app.route('/admin', methods = ['GET','POST'])
def admin():
    return admincontroller.adminPage(mysql)

@app.route('/dailyLogin', methods = ['GET','POST'])
def dailyLogin():
    return playercontroller.dailyLogin(mysql)

@app.route('/test', methods = ['GET','POST'])
def test():
    return playercontroller.test(mysql),200   


app.run(host='localhost', port=5000)