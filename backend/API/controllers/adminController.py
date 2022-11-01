#coding=windows-1252

from json.decoder import JSONDecodeError
from flask import request, render_template, session
import requests
import sys
import json
from os import listdir, rename
import json
from datetime import date

from werkzeug.utils import redirect

sys.path.append("../../AI")

from pic_taker import picTaker


class AdminController():
    def __init__(self):
        self.img_path_run = "static/characters/running_avatar/"
        self.img_path_idle= "static/characters/idle_avatar/"


    def statisticsPage(self,mysql):
        if not session.get('logged_in'):
            return redirect("/admin")

        users = []
        with mysql.connection.cursor() as cursor:
            playercount = cursor.execute('SELECT * FROM employee ') # Get total amount of employees (To be changed to players?)
            temp = cursor.fetchall()
            for row in temp:
                users.append(row[0:2])
            mysql.connection.commit

            # Grabbing how many unused characters are in folder.
        imagesList = [ x for x in listdir(self.img_path_run) if not x.startswith("emp_")]
        

        folders = listdir("images_ds")
        users_no_pictures = [x for x in users if str(x[0]) not in folders]
        local_news = []
        with open("themes/localNews.json", "r") as infile:
            try:
                json_obj = json.load(infile)
                news     = json_obj["news"]
                for key, value in news.items():
                    local_news.append(value)
            except JSONDecodeError:
                    print("The file is empty!")
        # Return Statistics page after sucessfull login
        return render_template('statistics.html', data=playercount, characters=len(imagesList), users=users_no_pictures, news=local_news)

    def adminPage(self):
        error = None
        if request.method == 'POST':
            with open("themes/adminCredentials.json", "r") as infile:
                json_obj = json.load(infile)
                credentials = json_obj["credentials"]
                username = credentials["username"]
                password = credentials["password"]
            if request.form['username'] == username and request.form['password'] == password:
                session['logged_in'] = True
            else:
                error = 'Invalid Credentials. Please try again.'
        
        if session.get('logged_in'):
            return render_template('index.html')

        return render_template('adminForm.html', error=error)

    def logout(self):
        session['logged_in'] = False
        return redirect("/admin")

    def deleteUserPage(self, mysql):
        if not session.get('logged_in'):
            return redirect("/admin")

        with mysql.connection.cursor() as cursor:
            sql = "SELECT emp_id, firstname, lastname FROM employee;"
            cursor.execute(sql)
            result = cursor.fetchall()

            if request.method == 'POST':
                emp_id  = request.form['emp_id']
                sql     = "SELECT emp_id, firstname, lastname FROM employee WHERE emp_id=%s;"
                cursor.execute(sql, (emp_id,))
                user = cursor.fetchone()
                deleted_user  = f"User {user[1]} {user[2]} with id {user[0]} has been removed from the database"
                query   = "DELETE FROM player WHERE emp_id=%s"
                cursor.execute(query, (emp_id,))

                images = [ x for x in listdir(self.img_path_run) if x.startswith("char_")]
                highest_index = -10
                for img in images:
                    temp = int(img[5:-4])
                    if temp > highest_index:
                        highest_index = temp

                new_index = highest_index+1

                running_avatars = [ x for x in listdir(self.img_path_run) if x.startswith("emp_")]
                idle_avatars    = listdir(self.img_path_idle)
                for i, filename in enumerate(running_avatars):
                    if "emp_"+emp_id+".gif" == filename:
                        print("Image:", self.img_path_run+filename," was renamed to => ", self.img_path_run+"char_"+str(new_index)+".gif")
                        rename(self.img_path_run+filename, self.img_path_run+"char_"+str(new_index)+".gif")
            
                for i, filename in enumerate(idle_avatars):
                    if "emp_"+emp_id+".gif" == filename:
                        print("Image:", self.img_path_idle+filename," was renamed to => ", self.img_path_idle+"char_"+str(new_index)+".gif")
                        rename(self.img_path_idle+filename, self.img_path_idle+"char_"+str(new_index)+".gif")
                
                query   = "DELETE FROM hero WHERE emp_id=%s"
                cursor.execute(query, (emp_id,))
                
                query   = "DELETE FROM employee WHERE emp_id=%s"
                cursor.execute(query, (emp_id,))
                mysql.connection.commit()
                return render_template('deleteUserForm.html', Deleted_user=deleted_user)


        return render_template('deleteUserForm.html', Data=result)

    # Adding a new user using requests.post
    def addUser(self):
        if not session.get('logged_in'):
            return redirect("/admin")

        error = "Error: "
        if request.method == 'POST':
            if len(request.form['firstname']) > 0:
                url         = 'http://localhost:5000/employee/create'
                firstname   = request.form['firstname']
                lastname    = request.form['lastname']
                birthdate   = request.form['birthdate']
                character   = request.form['characters']

                if len(birthdate) != 8:
                    error += f"Sorry! {birthdate} has the wrong format, please try with 4 digits of year, 2 digits for month, and 2 digits for day like YYYYMMDD, no spaces and no dashes."
                elif not birthdate.isdigit():
                    error+= f"Birthdate: [{birthdate}] has invalid characters, please use digits in format YYYYMMDD!"    
                    return render_template('addUser.html', Error=error)

                input_month = int(birthdate[4:6])
                input_day   = int(birthdate[-2:])

                if input_month > 12 or input_month < 0:
                    error += f"Month {input_month} is not an option! Please enter a month between 01 - 12"
                elif input_month == 2 and input_day > 29:
                    error += "February only has 28 sometimes 29 days, please enter a lower value!"
                elif (input_month % 2 == 0 and input_month < 7 or input_month % 2 == 1 and input_month > 8) and input_day > 30:
                    error += f"Sorry February, April, June, September, and November does not have {input_day} days, 30 is maximum"
                elif input_day > 31:
                    error += f"Sorry, no month has {input_day} days in it!"
           
                if error == "Error: ":
                    create_str = f"?firstname={firstname}&lastname={lastname}&birthdate={birthdate}&character={character}"
                    message = f"User [{firstname} {lastname}] with birthdate {birthdate} has been created"
                    res = requests.post(url+create_str)                        

                    return render_template('addUser.html', Data=message)

                return render_template('addUser.html', Error=error)
        
        #https://stackoverflow.com/questions/36774431/how-to-load-images-from-a-directory-on-the-computer-in-python
        imagesList = [ x for x in listdir(self.img_path_run) if not x.startswith("emp_")]
        
        if len(imagesList) == 0:
            error += "No more characters to use from, please add more characters to /static/characters!"
            return render_template('addUser.html', Error=error)
        else:
            return render_template('addUserForm.html', images=imagesList)
    
    
    def takePictures(self, mysql):
        if not session.get('logged_in'):
            return redirect("/admin")

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
        if not session.get('logged_in'):
            return redirect("/admin")

        result = ""
        if request.method == 'POST':
            with mysql.connection.cursor() as cursor:
                sql = request.form['query']
                cursor.execute(sql)
                result = cursor.fetchall()
                mysql.connection.commit()

        return render_template("sqlForm.html", Data=result)

    ''' Write or return theme configurations
    INPUT: configuration name (GET), configuration name and actual configuration (POST)
    OUTPUT: requested configuration (GET), Update message (POST)
    '''
    def theme(self):
        path = f"themes"
        
        if request.method == 'GET':
            configuration = str(request.args.get('config'))  
            with open(f"{path}/{configuration}.json", 'r') as openfile:
                json_object = openfile.read() 
            return json_object, 200

        if request.method == 'POST':
            configuration = str(request.args.get('config'))  
            text = request.get_json()
            with open(f"{path}/{configuration}.json", "w") as outfile:
#                 outfile.write(text)
                json.dump(text, outfile)
            return ("Themes Updated!",201)
        return 405

    def localNews(self):
        if not session.get('logged_in'):
            return redirect("/admin")

        path        = "themes"
        today       = date.today()
        now         = str(today)
        today_day   = now[-2:]
        text        = {}
        index       = 1
        news        = ""

        if request.method == 'POST':
            news = request.form["news"]
            date_in_file = ""
            day = 0
            with open(f"{path}/localNews.json", "r") as infile:
                try:
                    json_obj     = json.load(infile)
                    date_in_file = json_obj['date']
                    text['news'] = json_obj['news']
                    index = len(text['news']) + 1
                except JSONDecodeError:
                    print("The file is empty!")

                day = date_in_file[-2:]
                if day != today_day:
                    index = 1
                    with open(f"{path}/localNews.json", "w") as outfile:
                        outfile.write("")
                text['date'] = now
                if index == 1:
                    text['news'] = {index:news} 
                else: 
                    text['news'][index] = news
                with open(f"{path}/localNews.json", "w") as outfile:
                    json.dump(text, outfile, indent=2, ensure_ascii=False)
            
        return render_template("localNewsForm.html", Status=news)
            
# Create Admin Controller instance to use its functions
admincontroller = AdminController()       