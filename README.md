# DoggoCommand
## mac_joystick.py

Running this file with a joystick and xigbee module plugged in will allow for remote control of doggo

## install.sh

Running this installs the necessary libraries for runing mac_joystick.py

## csv2graph.py

Running this allows for easy graphing of csv data generally taken from doggo
The csv must have the names at the top of the columns and the file MUST be run
in python 2

## realtimeDataGrapher.py

Similar to csv2graph.py, this is meant for realtime data visualization
Plug in the zigbee module and watch whatever data you want to graph

UNTESTED

Input a tuple of the indexes of the data you want to see graph along with a name for the output CSV

If the graph window truncates too much data, change the constant at the top of the file (NUM_DATAPOINTS). The default is the last 20 datapoints
