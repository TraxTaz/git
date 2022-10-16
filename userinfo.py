from flask import Flask, render_template, redirect, request, flash
import csv

user_names = []
user_passwords = []

with open('login.csv', 'r') as filevar:
    reader = csv.reader(filevar)
    for row in reader:
        user_names.append(row[0])
        user_passwords.append(row[1])
    

app = Flask(__name__)
app.secret_key = b'balls'

@app.route('/')
def init():
    return render_template('login.html')

@app.route('/register')
def index2():
    return render_template('register.html')

@app.route('/login', methods = ['POST'])
def user_login():
    global userinfo

    username = request.form['username']
    userpass = request.form['userpass']

    userinfo = (username, userpass)

    for index in range(0, len(user_names)):
        for index2 in range(1,len(user_passwords)):
            if username == user_names[index]:
                if userpass == user_passwords[index2]:
                    return render_template('main.html')         
    else:
        flash ("Username is incorrect")
    return redirect ('/')

@app.route('/register.html')
def user_register():
        return render_template('register.html')

@app.route('/page', methods = ["POST"])
def register():
    global user_name, user_pass, user_info
    user_name = request.form['user_name']
    user_pass = request.form['user_pass']
    user_info = (user_name, user_pass)

    for index in range(0, len(user_names)):
           
        if user_name == user_names[index]:
            flash ("This username already exists")
            return render_template('register.html')
            break
    with open('login.csv', 'a+', newline= '') as filevar:
            info = user_name, user_pass
            writer = csv.writer(filevar, skipinitialspace=False)
            writer.writerow(info)
            user_names.append(user_name)
            user_passwords.append(user_pass)

    return redirect ('/')
