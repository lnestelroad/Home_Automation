#!/usr/bin/env python3

from flask import Flask, request, render_template, Response
import logging
import sys
import os
from time import time
from camera import VideoCamera

# sys.path.append("../Database")
# from db_interface import Database

app = Flask(__name__)

# Initiates logging module
# logging.basicConfig(filename="../GozerLogs/GozerWeb.log", filemode="a", level=logging.WARNING, format='%(asctime)s - %(levelname)s -%(message)s', datefmt='%d-%b-%y %H:%M:%S')

@app.route("/", methods=["GET", "POST"])
@app.route("/default")
def home():
    return render_template("base.html", rooms=["Liam's Room", "Isaac's Room"])

@app.route("/onButtonClick/", methods=['GET','POST'])
def buttonActions():
    """
        Summary: This function will hold all of buttons reaction code. By sending post requests, the decorator will redirect flask
            here where python will determine which button was pressed and then respond accordingly.
    """

    #TODO: add python scripts to operate circuitry here.

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

    elif request.form["submit_button"] == "Vacation":
        print ("Vacation Mode")

    return render_template("base.html", rooms=["Liam's Room", "Isaac's Room"])

@app.route("/cameraMovement/", methods=['GET', 'POST'])
def cameraMovement():
    
    if "up" in request.form:
        print ("up")
    
    elif "down" in request.form:
        print("down")

    return render_template("base.html", rooms=["Living Room", "Liam's Room", "Isaac's Room"])

@app.route("/lighting/", methods=['GET', 'POST'])
def lighting():
    select = request.form.get("Room")
    print(select)

    # TODO: take data from sql database and pass them to base.html
    return render_template("base.html", rooms=["Living Room", "Liam's Room", "Isaac's Room"])

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
  
@app.route('/video_feed/')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')    

if (__name__ == "__main__"):
    app.run(debug=True)