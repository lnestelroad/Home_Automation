#!/usr/bin/env python3

from flask import Flask, request, render_template
import sys
import os

# sys.path.append("../Database")
# from db_interface import Database


app = Flask(__name__)

@app.route("/")
@app.route("/default")
def home():
    return render_template('base.html')

@app.route("/open")
def open():
    return "Opening Door"

@app.route("/lock")
def lock():
    return "Locking Door"

@app.route("/who")
def who():
    return "Who's home"

@app.route("/see")
def seeFrontDoor():
    return "Front Door"

@app.route("/vacation")
def vacation():
    return "Vacation Mode"

if (__name__ == "__main__"):
    app.run(debug=True)