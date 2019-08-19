#!/usr/bin/env python3

################################## Comand to run #######################################
# python3 recognize_faces_video.py --encodings encodings.pickle \
#        --output output/webcam_face_recognition_output.avi --display 1 -mH 2 -mW 2
################################## Comand to run #######################################


# import the necessary packages
from imutils import build_montages
import face_recognition
import argparse
import imutils
import pickle
import time
from datetime import datetime
import numpy as np
import imagezmq.imagezmq.imagezmq as imagezmq
import cv2
import logging
import sys

sys.path.append("../Database")
from db_interface import Database

 
# sets up the logging stuff
logging.basicConfig(filename="../GozerLogs/GozerEntrance.log", filemode="a", level=logging.INFO, format='%(asctime)s - %(levelname)s -%(message)s', datefmt='%d-%b-%y %H:%M:%S')

# Configures the database
db = Database()
db.connectToDatabase()

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str,
	help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
	help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
ap.add_argument("-mW", "--montageW", required=True, type=int,
	help="montage frame width")
ap.add_argument("-mH", "--montageH", required=True, type=int,
	help="montage frame height")
args = vars(ap.parse_args())

# load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())
 
# initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
# initialize the ImageHub object
imageHub = imagezmq.ImageHub()
writer = None
frameDict = {}
mW = args["montageW"]
mH = args["montageH"]


# loop over frames from the video file stream
while True:
	# receive RPi name and frame from the RPi and acknowledge
	# the receipt
	(rpiName, frame) = imageHub.recv_image()
	imageHub.send_reply(b'OK')

	# update the new frame in the frame dictionary
	frameDict[rpiName] = frame

	# resize the frame to have a maximum width of 400 pixels, then
	# grab the frame dimensions and construct a blob
	
	# convert the input frame from BGR to RGB then resize it to have
	# a width of 750px (to speedup processing)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	rgb = imutils.resize(frame, width=400)
	r = frame.shape[1] / float(rgb.shape[1])
	(h, w) = rgb.shape[:2]
 
	# detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input frame, then compute
	# the facial embeddings for each face
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []

    	# loop over the facial embeddings
	for encoding in encodings:
		# attempt to match each face in the input image to our known
		# encodings
		matches = face_recognition.compare_faces(data["encodings"],
			encoding)
		name = "Unknown"
 
		# check to see if we have found a match
		if True in matches:
			
			# find the indexes of all matched faces then initialize a
			# dictionary to count the total number of times each face
			# was matched
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
			
			# loop over the matched indexes and maintain a count for
			# each recognized face face
			for i in matchedIdxs:
				name = data["names"][i]
				counts[name] = counts.get(name, 0) + 1
				
				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)

			#################################### PLACE REACTION CODE HERE ###################################################
			#TODO: Added scripts to activate locks

			if name != "Unknown":
				print("success {} from {}".format(name, rpiName))
				
				logging.info("{} Entering from {} at {}".format(name, rpiName, datetime.now()))
				db.addEntry(datetime.now(), rpiName, "Accepted", name)
				db.commitChanges()
				
				time.sleep(10)
			#################################################################################################################
				
		# update the list of names
		names.append(name)

    # loop over the recognized faces
	for ((top, right, bottom, left), name) in zip(boxes, names):
		# rescale the face coordinates
		top = int(top * r)
		right = int(right * r)
		bottom = int(bottom * r)
		left = int(left * r)
 
		# draw the predicted face name on the image
		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)

    # if the video writer is None *AND* we are supposed to write
	# the output video to disk initialize the writer
	if writer is None and args["output"] is not None:
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 20,
			(frame.shape[1], frame.shape[0]), True)
 
	# if the writer is not None, write the frame with recognized
	# faces to disk
	if writer is not None:
		writer.write(frame)

    # check to see if we are supposed to display the output frame to
	# the screen
	if args["display"] > 0:
		# build a montage using images in the frame dictionary
		montages = build_montages(frameDict.values(), (w, h), (mW, mH))
 
		# display the montage(s) on the screen
		for (i, montage) in enumerate(montages):
			# montage = imutils.rotate(montage, angle=90)
			cv2.imshow("Camera Feed", montage)

		key = cv2.waitKey(1) & 0xFF
 
		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

# do a bit of cleanup
cv2.destroyAllWindows()

# check to see if the video writer point needs to be released
if writer is not None:
	writer.release()
 