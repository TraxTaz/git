
from flask import Flask, render_template, redirect, request, flash
import csv

usern = []
userp = []

with open('login.csv', 'r') as filevar:
    reader = csv.reader(filevar)
    for row in reader:
        usern.append(row[0]),
        userp.append(row[0])
        

app = Flask(__name__)


@app.route('/')
def init():
    return render_template('login.html')


@app.route('/login', methods = ['POST'])
def user_login():
    global userinfo

    username = request.form['username']
    userpass = request.form['userage']

    userinfo = (username, userpass)
    if usern == username:
        with open ('login.csv', 'a+') as filevar:
            info = username, userpass
            writer = csv.writer(filevar, skipinitialspace=False)
            writer.writerow(info)
    if usern != username:
        flash ("Either Username or password incorrect")
        return render_template('hello.html')
    else:
        return redirect('/main')
        
@app.route('/register')
def index2():
    return render_template('Register.html')

@app.route('/register', methods = ['POST'])
def user_register():
    global user_name, user_pass, user_info
    user_name = request.form['user_name']
    user_pass = request.form['user_pass']

    user_info = (user_name, user_pass)
    return redirect('register')

@app.route('/main')
def index():
    (username, userpass) = userinfo
    return render_template('main.html', name = username, Pass = userpass)

@app.route('/register')
def index3():
    (user_name, user_pass) = user_info
    return render_template('Register.html', name2 = user_name, pass2 = user_pass)
