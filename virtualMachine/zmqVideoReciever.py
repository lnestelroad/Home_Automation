#!/usr/bin/env python3

#################################### Command to run #########################################
#       python3 zmqVideoReciever.py --montageW 2 --montageH 2                               #
#################################### Command to run #########################################

# import the necessary packages
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq.imagezmq.imagezmq as imagezmq
import argparse
import imutils
import cv2
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-mW", "--montageW", required=True, type=int,
	help="montage frame width")
ap.add_argument("-mH", "--montageH", required=True, type=int,
	help="montage frame height")
args = vars(ap.parse_args())

# initialize the ImageHub object
imageHub = imagezmq.ImageHub()
frameDict = {}
mW = args["montageW"]
mH = args["montageH"]
 
# start looping over all the frames
while True:
	# receive RPi name and frame from the RPi and acknowledge
	# the receipt
    (rpiName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')
    
    # resize the frame to have a maximum width of 400 pixels, then
	# grab the frame dimensions and construct a blob
    frame = imutils.resize(frame, width=400)
    (h, w) = frame.shape[:2]
    
    # update the new frame in the frame dictionary
    frameDict[rpiName] = frame
 
	# build a montage using images in the frame dictionary
    montages = build_montages(frameDict.values(), (w, h), (mW, mH))
 
	# display the montage(s) on the screen
    for (i, montage) in enumerate(montages):
        # montage = imutils.rotate(montage, angle=90)
        cv2.imshow("Home pet location monitor ({})".format(i),
			montage)
 
	# detect any kepresses
    key = cv2.waitKey(1) & 0xFF
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
	    break
 
# do a bit of cleanup
cv2.destroyAllWindows()