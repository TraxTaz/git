from flask import Flask, render_template, redirect, request, flash, url_for
import csv, random
import re
from statistics import *

Temp = 0
Time = 0
user_names = []
user_passwords = []
admins =["mario", "luigi"]
pizzas = {
    "Margharita": "tomato sauce, mozzarella and basil",
    "Napolitana": "raw tomatoes and mozzarella cheese",
    "Meat": "crumbled Italian sausage or ground beef bacon, pepperoni,and sliced ham",
    "Pepperoni": "tomato sauce, mozzarella and pepporoni",
    "Extra cheese": "tomato sauce, Extra cheese",
    "Veggie": "roasted red peppers, baby spinach, onions, mushrooms, tomatoes and black olives"
}
pp = []
pc = []
pv =[]
pm =[]
pma =[]
pbbq =[]
ordernumber =[]
#--------------Login---------------
with open('login.csv', 'r') as filevar:
    reader = csv.reader(filevar)
    for row in reader:
        user_names.append(row[0])
        user_passwords.append(row[1])

    with open('Sold.csv', 'r', newline="") as filevar:
     reader = csv.reader(filevar)
     for row in reader:
        pp.append(int(row[0]))
        pc.append(int(row[1]))
        pv.append(int(row[2]))
        pm.append(int(row[3]))
        pma.append(int(row[4]))
        pbbq.append(int(row[5]))
        ordernumber.append(int(row[6]))



app = Flask(__name__)
app.secret_key = b'balls'
#--------------------login-------------------------
@app.route('/login', methods = ['POST'])
def user_login():
    global userinfo

    username = request.form['username']
    userpass = request.form['userpass']

    userinfo = (username, userpass)

    for index in range(0, len(user_names)):
        if username == user_names[index]:
            if userpass == user_passwords[index]:
                if "Luigi" == user_names[index]:
                    return render_template('cook.html', username = username)
                if "Mario" == user_names[index]:
                    return render_template('cashier.html', username = username)
                return render_template('main.html', username = username)            
    else:
        flash ("Either username or password is incorrect")
        return redirect ('/userlogin')

#----------------Register--------------------
@app.route('/register')
def index2():
    return render_template('register.html')

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
    
    return redirect ('/userlogin')
#-------------------------pages--------------------------
@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/out')
def signout():
    return render_template('aboutusold.html')

@app.route('/out2')
def signout2():
    return render_template('locationold.html')

@app.route('/mainn')
def mains():
    return render_template('main.html')

@app.route('/orderhistory')
def ohistory():
    return render_template('orderhistory.html', Ordernumbers = ordernumber, pps = pp, pcs = pc, pvs = pv, pma = pma, pm = pm, pbbq = pbbq)

@app.route('/ovenstatus')
def ovenstatus():
    return render_template('ovenstatus.html', Temp = Temp, Time = Time, ordernumber = int(ordernumber[-1]),Pp = pp, Pc = pc, Pv = pv, Pm = pm, Pma = pma, Pbbq = pbbq)

@app.route('/current')
def currentorders():
    return render_template('currentorders.html',ordernumber = int(ordernumber[-1]),
    total = (pp[-1] * 8.99) + (pc[-1] * 6.99) + (pv[-1] * 7.99) + (pm[-1] * 9.99) + (pma[-1] * 8.99) + (pbbq[-1] * 8.99))

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/menu3')
def menu3():
    return render_template('menu3.html')

@app.route('/menulogin')    
def menulogon():
    return render_template('menu2.html')

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/userlogin')
def init():
    return render_template('login.html')

@app.route('/menulog')
def menulog():
    return render_template("menulog.html")

@app.route('/order')
def order():
    return render_template("order.html")

@app.route('/orderhistoryluigi')
def orderhistoryLuigi():
    return render_template('orderhistoryluigi.html', Ordernumbers = ordernumber, pps = pp, pcs = pc, pvs = pv, pma = pma, pm = pm, pbbq = pbbq)

@app.route('/ordersuccesful')
def ordersuccesful():
    return render_template('ordersuccesful.html',
    ordernumber = int(ordernumber[-1]),
    total = (pp[-1] * 8.99) + (pc[-1] * 6.99) + (pv[-1] * 7.99) + (pm[-1] * 9.99) + (pma[-1] * 8.99) + (pbbq[-1] * 8.99))
#--------------------arduino data------------------------
@app.route('/test', methods = ["POST"])
def send():
    global Time, Temp
    stats = request.get_json()
    Time = stats['time']
    Temp = stats['temp']
    return redirect('/ovenstatus')
#--------------------ordering system---------------------
@app.route("/buy")
def buy():
    return render_template('menu.html')

@app.route("/bought", methods=["POST"])
def bought():
    pp = int(request.form["PP"])
    pc = int(request.form["PC"])
    pv = int(request.form["PV"])
    pm = int(request.form["PM"])
    pma = int(request.form["PMA"])
    pbbq = int(request.form["PBBQ"])
    ordernumber = (random.randint(100000, 999999))

    Data = (pp, pc, pv, pm, pma, pbbq, ordernumber)
      
    with open('Sold.csv', 'a+', newline="") as textfile:
        writer = csv.writer(textfile, skipinitialspace=False)
        writer.writerow(Data)
    pp = []
    pc = []
    pv =[]
    pm =[]
    pma =[]
    pbbq =[]
    ordernumber =[]
    with open('Sold.csv', 'r', newline="") as filevar:
     reader = csv.reader(filevar)
     for row in reader:
        pp.append(float(row[0]))
        pc.append(float(row[1]))
        pv.append(float(row[2]))
        pm.append(float(row[3]))
        pma.append(float(row[4]))
        pbbq.append(float(row[5]))
        ordernumber.append(float(row[6]))
    return render_template('paying.html',
                        pp = int(pp[-1]),
                        pc = int(pc[-1]),
                        pv = int(pv[-1]),
                        pm = int(pm[-1]),
                        pma = int(pma[-1]),
                        pbbq = int(pbbq[-1]),
                        ordernumber = int(ordernumber[-1]),
                        total = (pp[-1] * 8.99) + (pc[-1] * 6.99) + (pv[-1] * 7.99) + (pm[-1] * 9.99) + (pma[-1] * 8.99) + (pbbq[-1] * 8.99)
)
@app.route("/paid")
def paid():
    pp = []
    pc = []
    pv =[]
    pm =[]
    pma =[]
    pbbq =[]
    ordernumber =[]
    with open('Sold.csv', 'r', newline="") as filevar:
     reader = csv.reader(filevar)
     for row in reader:
        pp.append(float(row[0]))
        pc.append(float(row[1]))
        pv.append(float(row[2]))
        pm.append(float(row[3]))
        pma.append(float(row[4]))
        pbbq.append(float(row[5]))
        ordernumber.append(float(row[6]))
    return render_template('paid.html',
    ordernumber = int(ordernumber[-1]),
    total = (pp[-1] * 8.99) + (pc[-1] * 6.99) + (pv[-1] * 7.99) + (pm[-1] * 9.99) + (pma[-1] * 8.99) + (pbbq[-1] * 8.99)
)