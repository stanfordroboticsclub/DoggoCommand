#PYTHON 3
#Assumes the micro is printing a comma seperated list with a space
#e.i.
#2.3, 4.234, 5432445.34523, etc

#CHANGE SERIAL PORT BAUD RATE AND PORT PATH
#If problems parsing data, check the .split on line 21

import numpy as np
import math
import random
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial
import datetime as dt


NUM_DATAPOINTS = 100
outputChannels = (15,)

def animate(i, ser, data, timeArray, ax, outputChannels):
	line = ser.readline().decode("utf-8").strip()
	currentLine = line.split("\t")
	print(currentLine)
	for i in range(0, len(data)):
		data[i].append(float(currentLine[i]))

	timeArray.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
	ax.clear()

	for i in outputChannels:
		ax.plot(timeArray[-NUM_DATAPOINTS:], data[i][-NUM_DATAPOINTS:])

	plt.tick_params(
		axis='x',          # changes apply to the x-axis
		which='both',      # both major and minor ticks are affected
		bottom=False,      # ticks along the bottom edge are off
 		top=False,         # ticks along the top edge are off
		labelbottom=False)
	plt.xticks(rotation=45, ha='right')
	plt.subplots_adjust(bottom=0.30)
	plt.title('Data over Time')
	plt.ylabel('Data')
	plt.xlabel('Time')




def main():
	data = []

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	timeArray = []

	csvFileName = input("CSV output file name (ending in .csv): ")


	#nano is 9600, teensy is 115200
	with serial.Serial('/dev/cu.usbserial-DN042CH3', 115200, timeout=1) as ser:
		time.sleep(.5)

		line = ser.readline().decode("utf-8").strip()
		for element in line.split("\t"):
			data.append([])
		#last entry doesn't have a comma
		ani = animation.FuncAnimation(fig, animate, fargs=(ser, data, timeArray, ax, outputChannels), interval=1)
		plt.show()

	with open(csvFileName, 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerows(data)
	csvFile.close()


if __name__ == "__main__":
	main()

