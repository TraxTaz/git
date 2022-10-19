from itertools import count
from flask import Flask, redirect, url_for, render_template, request
import csv
from statistics import *
import random
from tkinter import *

app = Flask(__name__)

counter = 0
#--------Login--------------------------------------

@app.route ("/")
def home():
    return render_template("index.html")

@app.route ("/signout")
def signout():
    return render_template("signout.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
       user = request.form["nm"]
       return redirect ("/signout")
    else:
      return render_template("login.html")

#--------Login--------------------------------------

#--------Buying system------------------------------
@app.route("/buy")
def buy():
    return render_template('buying.html')

@app.route("/bought", methods=["POST", "GET"])
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
                        totalpp = (pp[-1] * 7.50),
                        totalpc = (pp[-1] * 7.25),
                        totalpv = (pp[-1] * 8),
                        totalpm = (pp[-1] * 8),
                        totalpma = (pp[-1] * 8),
                        totalpbbq = (pp[-1] * 8),
                        total = (pp[-1] * 7.50) + (pc[-1] * 7.25) + (pv[-1] * 8) + (pm[-1] * 8) + (pma[-1] * 8) + (pbbq[-1] * 8),
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
    total = (pp[-1] * 7.50) + (pc[-1] * 7.25) + (pv[-1] * 8) + (pm[-1] * 8) + (pma[-1] * 8) + (pbbq[-1] * 8),
    )

#--------Buying system------------------------------
