#!/bin/bash

######################################################################################################
# Summary: This script will hold all of the configurations for opening the door, blinds, and garage. #
#   Via command line arguments, a specific location will be braught in so that the script know which #
#   location to activate and which action to perform.                                                #
#                                                                                                    #
# NOTE: as more devices are added, this file will need to be expanded upon until an option for this  #
#   can be implemented in the GUI.                                                                   #
#                                                                                                    #
# Command to run: sh commands.sh <location(s)>                                                       #
#                                                                                                    #
# Locations:                                                                                         #
#   frontDoor                                                                                        #
#   backDoor                                                                                         #
#   garageDoor                                                                                       #
#   blinds                                                                                           #
######################################################################################################

#
# Example of getopt (enhanced) approach to handling bash command-line arguments
#
# Original author: Robert Siemer
# Adapted by: Nicholas Zimmerer
# Modified by: Liam Nestelroad
#
# Reference: https://stackoverflow.com/a/29754866
#

# Check if system has getopt (enhanced)
getopt --test > /dev/null
if [[ $? -ne 4 ]]; then
    echo "\`getopt --test\` failed: this environment does appear to support getopt (enhanced)"
    exit 1
fi

# To be displayed when script is invoked incorrectly
# NOTE: tabs between -END and END are ignored, spaces are preserved.
USAGE=$(cat <<-END
usage: arguments.sh [OPTION]... FILE
​
Runs scripts on remote machines for operating home automation units. [BRACKETS] indicate an optional argument,
while ARGUMENTS without brackets are required. Ellipsis ... indicate multiple
arguments are accepted.

OPTIONS:
  [-l, --location]          text which will hold the location being activated
  [-a, --action]            integer to indecate what action to perform at the location

  -h, --help                display this help and exit
  -v, --verbose             explain what is being done
END
)

# describe the valid short (single letter) & long options 
# NOTE a: this option can only take 1 or 0. should be in form '-a 1'
# NOTE l: designates the desired location for. Should be in form '-l frontDoor'

# NOTE: the : after a and l indicate that these flags take some kind of input
OPTIONS=l:a:hv
LONGOPTIONS=location,action,help:,verbose

# PARSED stores the output, in case of errors
# using the `--options` keyword invokes enhanced mode
# using `-- "$@"` ensures correct quotation interpretation
PARSED=$(getopt --options=$OPTIONS --longoptions=$LONGOPTIONS --name "$0" -- "$@")
if [[ $? -ne 0 ]]; then
    # $? is a special variable that stored the most recent exit code
    # In UNIX, non-zero exit codes indicate errors, while 0 indicates success
    exit 2
fi

# by reading the output this way, quoting is parsed correctly
eval set -- "$PARSED"

locationFlag=false
actionFlag=false

# now we can case/match on the arguments in an organized manner
while true; do
    case "$1" in
        -h|--help)
            echo "$USAGE"
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        -l|--location)  # gets the specific location passed in. $2 is the location
            LOC=$2
            locationFlag=true
            shift 2
            ;;
        -a|--action)    # gets the actions requested
            ACT="$2"
            actionFlag=true
            shift 2
            ;;
        --)         # separates non-option arguments from the short/long options
            shift
            break
            ;;
        *)          # Acts as a catch-all, like an "else"
            echo "Programming error"
            echo "$USAGE"
            exit 3
            ;;
    esac
done

# # handle non-option arguments
# if [[ $# -ne 1 ]]; then     # bash special variable `$#` expands positional parameters
#     echo "$0: Single input file is required"
#     exit 4
# fi

# Determines what action was requested
if [[ $ACT -eq 1 ]]; then
    ACT="Opening"
elif [[ $ACT -eq 0 ]]; then
    ACT="Closing"
else
    echo "action must either be a 1 for open or 0 for close"
    exit 2
fi

# Determines if location and action flags were used
if ! $actionFlag && !$locationFlag; then
    echo "-a and -l flags are required"
    exit 1
fi

# Executes location specific script 
case "$LOC" in
    frontDoor)
        ssh pi3 'bash -s' < ../actions/frontDoor.sh $ACT
        ;;
    backDoor)
        ssh pi3 'bash -s' < ../actions/backDoor.sh $ACT
        ;;
    garage)
        ssh pi3 'bash -s' < ../actions/garageDoor.sh $ACT
        ;;
    frontBlinds)
        ssh pi3 'bash -s' < ../actions/frontBlinds.sh $ACT
        ;;
    backBlinds)
        ssh pi3 'bash -s' < ../actions/backBlinds.sh $ACT
        ;;
    liamsBlinds)
        ssh pi3 'bash -s' < ../actions/liamsBlinds.sh $ACT
        ;;
    vacation)
        ssh pi3 'bash -s' < ../actions/vacation.sh $ACT
        ;;
    *)
        echo "No location specified"
        exit 2
        ;;
esac

# Display the result of passed arguments
if [[ $VERBOSE -eq 1 ]]; then
    printf "\nVerbose output set:\n"  
fi

# Display verbose output, if VERBOSE flag set
if [[ $VERBOSE -eq 1 ]]; then

    # prints the action and location
    printf "\t$ACT $LOC\n"
fi

# # After all out shifts, the only remaining parameter is FILE, located at $1
# if [[ -f $1 ]]; then
#     echo "$1: File found!"
# else
#     echo "$1: Could not find file..."
# fi
