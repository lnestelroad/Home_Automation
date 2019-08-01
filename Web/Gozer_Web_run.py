#!/usr/bin/env python3

from flask import Flask, request, render_template
import sys
import os

sys.path.append("../Database")
from db_interface import Database


app = Flask(__name__)

@app.route("/")
@app.route("/default")
def home():
    return render_template('base.html')

if (__name__ == "__main__"):
    app.run(debug=True)