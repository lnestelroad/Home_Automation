#!/usr/bin/env python3

import os
import sys
import logging
import subprocess
from time import time
from datetime import datetime
from camera import VideoCamera
from flask import Flask, request, render_template, Response

# sys.path.append("../Database")
# from db_interface import Database

app = Flask(__name__)

# Initiates logging module
logging.basicConfig(filename="/home/liam_work/Documents/Home_Automation/GozerLogs/GozerWeb.log", filemode="a", level=logging.WARNING, format='%(asctime)s - %(levelname)s -%(message)s', datefmt='%d-%b-%y %H:%M:%S')

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
    # Changes directory to the files location
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)

    # Determines which button was pressed then activates the motion scripts
    if request.form["submit_button"] == "Open Front Door":
        print ("Opening Front Door")
        subprocess.check_call("./commands.sh %s %s" % ("-a 1", "-l frontDoor"), shell=True)
        logging.warning("Front door opened at {}".format(datetime.now()))

    elif request.form["submit_button"] == "Lock Front Door":
        print ("Locking Front Door")
        subprocess.check_call("./commands.sh %s %s" % ("-a 0", "-l frontDoor"), shell=True)
        logging.warning("Front door opened at {}".format(datetime.now()))

    elif request.form["submit_button"] == "Open Garage Door":
        print ("Opening Garage Door")
        subprocess.check_call("./commands.sh %s %s" % ("-a 1", "-l garage"), shell=True)
        logging.warning("Front door opened at {}".format(datetime.now()))

    elif request.form["submit_button"] == "Close Garage Door":
        print ("Closing Garage Door")
        subprocess.check_call("./commands.sh %s %s" % ("-a 0", "-l garage"), shell=True)
        logging.warning("Front door opened at {}".format(datetime.now()))

    elif request.form["submit_button"] == "Open Blinds":
        print ("Opening Blinds")
        subprocess.check_call("./commands.sh %s %s" % ("-a 1", "-l frontBlinds"), shell=True)
        logging.warning("Front door opened at {}".format(datetime.now()))

    elif request.form["submit_button"] == "Close Blinds":
        print ("Closing Blinds")
        subprocess.check_call("./commands.sh %s %s" % ("-a 0", "-l frontBlinds"), shell=True)
        logging.warning("Front door opened at {}".format(datetime.now()))

    elif request.form["submit_button"] == "Vacation":
        print ("Vacation Mode")
        subprocess.check_call("./commands.sh %s %s" % ("-a 1", "-l vacation"), shell=True)
        logging.warning("Front door opened at {}".format(datetime.now()))
        
    return render_template("base.html", rooms=["Liam's Room", "Isaac's Room"])

@app.route("/cameraMovement/", methods=['GET', 'POST'])
def cameraMovement():
    
    if "up" in request.form:
        print ("up")
    
    elif "down" in request.form:
        print("down")
    
    elif "right" in request.form:
        print ("right")

    elif "left" in request.form:
        print ("left")

    return render_template("base.html", rooms=["Living Room", "Liam's Room", "Isaac's Room"])

@app.route("/lighting/", methods=['GET', 'POST'])
def lighting():
    select = request.form.get("Room")
    print(select)

    # TODO: take data from sql database and pass them to base.html
    return render_template("base.html", rooms=["Living Room", "Liam's Room", "Isaac's Room"])

def gen(camera):
    try:
        while True:
            frame = camera.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except:
        return "failed"
  
@app.route('/video_feed/')
def video_feed():
    try:
        return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')    
    except:
        return "failed"

if (__name__ == "__main__"):
    app.run(debug=True)