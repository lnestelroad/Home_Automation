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

t_end = time.time() + 60 
# while time.time() < t_end:
while True:
    # read the frame from the camera and send it to the server
    frame = vs.read()
    reply = sender.send_image(rpiName, frame)
    if reply.decode("utf-8") == "Open Door":
        print("Opening Door")
        print(" ______________\n\
|\ ___________ /|\n\
| |  /|,| |   | |\n\
| | |,x,| |   | |\n\
| | |,x,' |   | |\n\
| | |,x   ,   | |\n\
| | |/    |%==| |\n\
| |    /] ,   | |\n\
| |   [/ ()   | |\n\
| |       |   | |\n\
| |       |   | |\n\
| |       |   | |\n\
| |      ,'   | |\n\
| |   ,'      | |\n\
|_|,'_________|_|")

        time.sleep(5)
        print("Closeing Door")
        print(" ______________\n\
|\ ___________ /|\n\
| |  _ _ _ _  | |\n\
| | | | | | | | |\n\
| | |-+-+-+-| | |\n\
| | |-+-+=+%| | |\n\
| | |_|_|_|_| | |\n\
| |    ___    | |\n\
| |   [___] ()| |\n\
| |         ||| |\n\
| |         ()| |\n\
| |           | |\n\
| |           | |\n\
| |           | |\n\
|_|___________|_|")
