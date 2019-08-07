#!/usr/bin/env python3

############################## Command to run ##################################
# python3 zmqLiveStream.py -s 10.203.177.15                                    #
############################## Command to run ##################################

import imagezmq
import argparse
import socket
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--server-ip", required=True,
	help="ip address of the server to which the client will connect")
args = vars(ap.parse_args())
 
# initialize the ImageSender object with the socket address of the
# server
sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(args["server_ip"]))

rpiName = socket.gethostname()
vs = imagezmq.VideoStream(usePiCamera=True).start()
#vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
	# read the frame from the camera and send it to the server
	frame = vs.read()
	sender.send_image(rpiName, frame)
