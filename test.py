from flask import Flask, render_template, redirect, flash, request_started

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('')