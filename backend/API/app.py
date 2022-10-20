from flask import Flask
from flask_mysqldb import MySQL
from controllers.employeeController import employeecontroller
from controllers.adminController import admincontroller
from controllers.playerController import playercontroller
from flask_cors import CORS

# 'Production' Configuration
db_password    = ''
db_name        = 'sims'

# Define App and open connection to the mysql database
def createApp(db_password, db_name):
    app = Flask(__name__)
    app.config['MYSQL_HOST']        = 'localhost'
    app.config['MYSQL_USER']        = 'root'
    app.config['MYSQL_PASSWORD']    = db_password
    app.config['MYSQL_DB']          = db_name
    return app
    
app = createApp(db_password,db_name)   
mysql = MySQL(app)

CORS(app)

'''
EMPLOYEE ROUTES
'''
# Route to create employees and get their name based on ID
@app.route('/employee/create', methods = ['POST'])
def employee():
    return employeecontroller.createEmployee(mysql)

'''
ADMIN ROUTES
'''
# Route for admin to see statistics     
@app.route('/admin', methods = ['GET','POST'])
def admin():
    return admincontroller.adminPage()

@app.route('/admin/statistics', methods = ['GET', 'POST'])
def statistics():
    return admincontroller.statisticsPage(mysql)

@app.route('/admin/addUser', methods = ['GET', 'POST'])
def addUser():
    return admincontroller.addUser()

@app.route('/admin/deleteUser', methods = ['GET', 'POST'])
def deleteUser():
    return admincontroller.deleteUserPage(mysql)

@app.route('/admin/takePictures', methods = ['GET', 'POST'])
def takePictures():
    return admincontroller.takePictures(mysql)

@app.route('/admin/sql', methods = ['GET', 'POST'])
def sendSQL():
    return admincontroller.sendSQL(mysql);

@app.route('/admin/addUser/characters', methods = ['GET', 'POST'])
def showCharacters():
    return admincontroller.showCharacters()

@app.route('/admin/theme', methods = ['GET','POST'])
def theme():
    return admincontroller.theme() 

'''
PLAYER ROUTES
'''
# Route to register Players that were recently recognized by the AI
@app.route('/player/newEntry', methods = ['POST'])
def newEntries():
    return playercontroller.newEntry(mysql)

# Route used to log in, and get JSON Info on all recently recognized players, called by the frontend
@app.route('/player/getRecent', methods = ['GET'])
def getRecent():
    return playercontroller.getRecent(mysql)    

# Route to get last months heroes (top 3 most monthly XP), as well as the current Top player
@app.route('/player/getTop', methods = ['GET'])
def getTop():
    return playercontroller.getTop(mysql)        

# Route to All Employee IDs and corresponding Monthly XP
@app.route('/player/getMonthlyXP', methods = ['GET'])
def getMonthlyXP():
    return playercontroller.getMonthlyXP(mysql)   

app.run(host='localhost', port=5000)
