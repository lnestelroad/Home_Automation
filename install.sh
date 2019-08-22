#!/bin/bash

##################################################################
# Install.sh                                                     #
#   This script is used for installing the home automation unit  #
#                                                                #
#   Author: Liam Nestelroad                                      #
#                                                                #
#   Command to run: ./install.sh                                 #
##################################################################

echo "Welcome to the home automation kit!"

encodeFile=$(dirname $(readlink -f ./install.sh))
cd "$encodeFile/Database"
python3 db_interface.py -b 1

mkdir ../Facial_Recognition/dataset