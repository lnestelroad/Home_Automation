#!/bin/bash

encodeFile=$(readlink -f ../Facial_Recognition/restart_system.sh)
cd $(dirname $encodeFile)

python3 recognize_faces_video.py --encodings encodings.pickle \
        --output output/webcam_face_recognition_output.avi --display 1 -mH 2 -mW 2

ssh pi