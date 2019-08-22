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

# Gets all of the required python packages
pip3 install -r requirements.txt

# Finds the directory of the current file
encodeFile=$(dirname $(readlink -f ./install.sh))
cd "$encodeFile/Database"

# Builds the database for the first time
python3 db_interface.py -b 1

# Makes a directory that git could not save
mkdir ../Facial_Recognition/dataset