#!/bin/bash

encodeFile=$(readlink -f ../Facial_Recognition/encode_faces.py)

cd $(dirname $encodeFile)
python3 encode_faces.py --dataset dataset --encodings encodings.pickle