from flask import request, render_template
import requests
import sys
import json
from os import listdir, rename

sys.path.append("../../AI")

from pic_taker import picTaker


# PETER [22-10-11]
# I will need to add character when creating a new user
# The user should be able to see what character to choose from
# When deleting character I will have to DELETE from Hero and emp_char first!


class AdminController():
    def __init__(self):
        self.img_path_run = "static/characters/running_avatar/"
        self.img_path_idle= "static/characters/idle_avatar/"

    def statisticsPage(self,mysql):
        cursor = mysql.connection.cursor()
        playercount = cursor.execute('SELECT * FROM employee ') # Get total amount of employees (To be changed to players?)
        mysql.connection.commit()
        cursor.close()
        return render_template('statistics.html', data=playercount) # Return Statistics page after sucessfull login

    def adminPage(self):
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' or request.form['password'] != 'admin': # Check user input against hard-coded password
                error = 'Invalid Credentials. Please try again.'
            else:
                return render_template('index.html')
        return render_template('adminForm.html', error=error)

    def deleteUserPage(self, mysql):
        print("request: ", request.method)
        with mysql.connection.cursor() as cursor:
            sql = "SELECT emp_id, firstname, lastname FROM employee;"
            cursor.execute(sql)
            result = cursor.fetchall()

            if request.method == 'POST':
                emp_id  = request.form['emp_id']
                sql     = "SELECT emp_id, firstname, lastname FROM employee WHERE emp_id=%s;"
                cursor.execute(sql, (emp_id,))
                user = cursor.fetchone()
                #print("user: ", user)
                deleted_user  = f"User {user[1]} {user[2]} with id {user[0]} has been removed from the database"
                #print("deleted_user: ", deleted_user)
                query   = "DELETE FROM player WHERE emp_id=%s"
                cursor.execute(query, (emp_id,))

                images = [ x for x in listdir(self.img_path_run) if x.startswith("char_")]
                highest_index = -10
                for img in images:
                    temp = int(img[5:-4])
                    if temp > highest_index:
                        highest_index = temp

                new_index = highest_index+1
                print("highest_index: ",highest_index)

                running_avatars = [ x for x in listdir(self.img_path_run) if x.startswith("emp_")]
                idle_avatars    = listdir(self.img_path_idle)
                for i, filename in enumerate(running_avatars):
                    print("filename: ", filename)
                    if "emp_"+emp_id+".gif" == filename:
                        print("Image:", self.img_path_run+filename," was renamed to => ", self.img_path_run+"char_"+str(new_index)+".gif")
                        rename(self.img_path_run+filename, self.img_path_run+"char_"+str(new_index)+".gif")
            
                for i, filename in enumerate(idle_avatars):
                    if "emp_"+emp_id+".gif" == filename:
                        print("Image:", self.img_path_idle+filename," was renamed to => ", self.img_path_idle+"char_"+str(new_index)+".gif")
                        rename(self.img_path_idle+filename, self.img_path_idle+"char_"+str(new_index)+".gif")
                
                #query   = "DELETE FROM hero WHERE emp_id=%s"
                #cursor.execute(query, emp_id)
                
                query   = "DELETE FROM employee WHERE emp_id=%s"
                cursor.execute(query, (emp_id,))
                mysql.connection.commit()
                return render_template('deleteUserForm.html', Deleted_user=deleted_user)


        return render_template('deleteUserForm.html', Data=result)

    # Adding a new user using requests.post
    def addUser(self):
        error = "Error:"
        if request.method == 'POST':
            if len(request.form['firstname']) > 0:
                url         = 'http://localhost:5000/employee/create'
                firstname   = request.form['firstname']
                lastname    = request.form['lastname']
                birthdate   = request.form['birthdate']
                character   = request.form['characters']

                print("character: ", character)

                if len(birthdate) != 8:
                    error += "Sorry! Birthdate has the wrong format, please try with 4 digits of year, 2 digits for month, and 2 digits for day like YYYYMMDD, no spaces and no dashes."
                #elif birthdate.find('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#"%&/()=?@${[]}\'~^*'):
                    #error+= "Invalid characters in birthdate!"    
                    return render_template('addUser.html', Error=error)

                input_month = int(birthdate[4:6])
                input_day   = int(birthdate[-2:])

                if input_month > 12 or input_month < 0:
                    error += "Month {} is not an option! Please enter a month between 01 - 12".format(input_month)
                elif input_month == 2 and input_day > 29:
                    error += "February only has 28 sometimes 29 days, please enter a lower value!"
                elif (input_month % 2 == 0 and input_month < 7 or input_month % 2 == 1 and input_month > 8) and input_day > 30:
                    error += "Sorry February, April, June, September, and November does not have {} days, 30 is maximum".format(input_day)
                elif input_day > 31:
                    error += "Sorry, no month has {} days in it!".format(input_day)
           
                if error == "Error:":
                    create_str = f"?firstname={firstname}&lastname={lastname}&birthdate={birthdate}&character={character}"
                    message = f"User [{firstname} {lastname}] with birthdate {birthdate} has been created"
                    res = requests.post(url+create_str)                        

                    return render_template('addUser.html', Data=message)
                print("error: ", error)
                return render_template('addUser.html', Error=error)
        
        #https://stackoverflow.com/questions/36774431/how-to-load-images-from-a-directory-on-the-computer-in-python
        imagesList = [ x for x in listdir(self.img_path_run) if not x.startswith("emp_")]
        
        if len(imagesList) == 0:
            error += "No more characters to use from, please add more characters to /static/characters!"
            return render_template('addUser.html', Error=error)
        else:
            return render_template('addUserForm.html', images=imagesList)
    
    
    def takePictures(self, mysql):
        with mysql.connection.cursor() as cursor:
            sql = "SELECT emp_id, firstname, lastname FROM employee ORDER BY emp_id DESC LIMIT 5"
            cursor.execute(sql)
            users = cursor.fetchall()
            message = ""

            if request.method == 'POST':
                emp_id          = request.form['emp_id']
                amount_pictures = request.form['pictures']
                
                if amount_pictures == "":
                    message = f"1000 pictures has been taken of ID: {emp_id}!"
                    picTaker(emp_id)
                else:
                    message = f"{amount_pictures} pictures has been taken of ID: {emp_id}!"
                    picTaker(emp_id, int(amount_pictures))
                return render_template('picTaker.html', Status=message)

            return render_template('picTaker.html', Data=users)
    
    def sendSQL(self, mysql):
        if request.method == 'POST':
            pass
        else:
            return render_template("sqlForm.html")

    ''' Write or return theme configurations
    INPUT: configuration name (GET), configuration name and actual configuration (POST)
    OUTPUT: requested configuration (GET), Update message (POST)
    '''
    def theme(self):
        path = f"themes"
        
        if request.method == 'GET':
            configuration = str(request.args.get('config'))  

            with open(f"{path}/{configuration}.json", 'r') as openfile:
                json_object = json.load(openfile) 
            return json_object, 200

        if request.method == 'POST':
            configuration = str(request.args.get('config'))  
            text = request.get_json()
            with open(f"{path}/{configuration}.json", "w") as outfile:
                outfile.write(str(text))
            return ("Themes Updated!",201)

        return 405
            
# Create Admin Controller instance to use its functions
admincontroller = AdminController()       