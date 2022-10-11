from flask import Flask
from flask_mysqldb import MySQL
from controllers.employeeController import employeecontroller
from controllers.adminController import admincontroller
from controllers.playerController import playercontroller


db_password    = ''
db_name        = 'sims'

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

# Route to register Players that were recently recognized by the AI
@app.route('/player/newEntry', methods = ['POST'])
def newEntries():
    return playercontroller.newEntry(mysql)

# Route used to log in, and get JSON Info on all recently recognized players, called by the frontend
@app.route('/player/getRecent', methods = ['GET'])
def getRecent():
    return playercontroller.getRecent(mysql)    

app.run(host='localhost', port=5000)
