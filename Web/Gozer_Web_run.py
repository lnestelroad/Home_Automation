#!/usr/bin/env python3

from flask import Flask, request, render_template
import logging
import sys
import os

# sys.path.append("../Database")
# from db_interface import Database


app = Flask(__name__)

# Initiates logging module
# logging.basicConfig(filename="../GozerLogs/GozerWeb.log", filemode="a", level=logging.WARNING, format='%(asctime)s - %(levelname)s -%(message)s', datefmt='%d-%b-%y %H:%M:%S')

@app.route("/", methods=["GET", "POST"])
@app.route("/default")
def home():
    return render_template('base.html')

@app.route("/onButtonClick/", methods=['GET','POST'])
def buttonActions():
    """
        Summary: This function will hold all of buttons reaction code. By sending post requests, the decorator will redirect flask
            here where python will determine which button was pressed and then respond accordingly.
    """

    if request.form["submit_button"] == "Open Front Door":
        print ("Opening Front Door")

    elif request.form["submit_button"] == "Open Garage Door":
        print ("Opening Garage Door")

    elif request.form["submit_button"] == "Lock Front Door":
        print ("Locking Front Door")

    elif request.form["submit_button"] == "Close Garage Door":
        print ("Closing Garage Door")

    elif request.form["submit_button"] == "Open Blinds":
        print ("Opening Blinds")

    elif request.form["submit_button"] == "Close Blinds":
        print ("Closing Blinds")

    return render_template("base.html")

if (__name__ == "__main__"):
    app.run(debug=True)