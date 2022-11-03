# importing libraries
from asyncore import write
import time, sys
from fhict_cb_01.CustomPymata4 import CustomPymata4
from flask import Flask
import requests
import csv

# Define variables

LEFT_BUTTON = 9
RIGHT_BUTTON = 8
GREEN_LED = 5
RED_LED = 4
BUTTON_PRESSED = 0
num = 0
sound = 3
lTime =[]
lTemp = []
maxTemp = 500
app = Flask(__name__)



# send the data to the server
def send():
    global response
    data = {'time': lTime, 'temp': lTemp}
    response = requests.post('http://145.93.76.200:5000/test', json = data)


# starting the board
def start_up():
    global board
    board = CustomPymata4("COM3")
    time.sleep(2)
    board.set_pin_mode_digital_input_pullup(LEFT_BUTTON) 
    board.set_pin_mode_digital_input_pullup(RIGHT_BUTTON) 
    board.set_pin_mode_pwm_output(sound)
    board.displayOn()
    time.sleep(1)

# activate the buzzer and light when timer is up
def buzz():
    board.digital_pin_write(GREEN_LED,1)
    for i in range(5):
        board.digital_pin_write(GREEN_LED,1)
        board.pwm_write(sound,1)
        time.sleep(0.6)
        board.digital_pin_write(GREEN_LED,0)
        board.pwm_write(sound,0)
        time.sleep(0.6)
    
        
# what will happen when the time is up
def afterC():
        time.sleep(1)
        status = 'Pizza is ready!'
        print(status)
        board.digital_pin_write(RED_LED,0)
        board.displayShow('0.0.0.0') 
        buzz()
        time.sleep(0.01)
        board.digital_pin_write(GREEN_LED,1)
        time.sleep(0.01)
           


# define the countdown function
def countdown(t):
    
    while t:
        # starting the countdown and converting the numbers into timer
        mins, secs = divmod(t, 60)
        timer = '{:02d}.{:02d}'.format(mins, secs)
        time.sleep(1)
        t -= 1
        board.displayShow(timer)
        board.digital_pin_write(RED_LED, 1)
        board.digital_pin_write(GREEN_LED,0)
        print(timer, end="\r")
        status = 'Pizza is cooking.'
        print(status, end='\r')
        lTime.append(timer)
        data2 = (lTime)
        # sending the data to a csv file
        with open('data.csv', 'a+', newline="") as textfile:
            writer = csv.writer(textfile, skipinitialspace=False)
            writer.writerow(data2)
            textfile.close()
        lTime.pop(0)
    # what happens when the countdown is complete \
        
    afterC()
    
# how the oven works
def oven():
    global num, t
    while True:
       
        buttonState = board.digital_read(LEFT_BUTTON)
        buttonState2 = board.digital_read(RIGHT_BUTTON)
        time.sleep(0.10)
        # setting a temperature when the left button is pressed
        if(buttonState[0] == BUTTON_PRESSED):
            board.digital_write(GREEN_LED,0)
            board.displayOn()
            while True:
                num = float(input("Input temperature for the pizza: "))
                if (num > maxTemp):
                    print("The temperature should be less then 500 degrees!")
                else:
                    break; 
            board.displayShow(num)
            lTemp.append(num)     
            
                       
        # setting a time for the oven when the right button is pressed and timer starts
        if (buttonState2[0] == BUTTON_PRESSED):
            board.displayOn()
            tm = int(input("Enter time in minutes: "))*60
            ts = int(input("Enter time in seconds: "))
            t = tm + ts
            countdown(int(t))
            num = 0
        # sending the data to a csv file
        data = (lTemp)
        with open('data.csv', 'a+', newline="") as textfile:
            writer = csv.writer(textfile, skipinitialspace=False)
            writer.writerow(data)
            textfile.close()
        
        send() #uncomment this to send the data to the server (when the server is working)
    
            
start_up()
oven()
