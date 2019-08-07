import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

while True:
    #  Wait for next request from client
    message = socket.recv()
    print ("Received request: ", message)
    time.sleep (1)
    socket.send_string("World from %s" % port)
