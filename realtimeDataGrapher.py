#PYTHON 3
#Change consts if not working
#Assumes data is comma seperated with no ws besides \n e.i.:
#1,2,3,41234,12351,1378534,452,4626
#Only issue is that each graphing period will not save that data to the output,
#This isn't too bad since there are so many datapoints tho


import numpy as np
import math
import random
import csv
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial
import datetime as dt
import threading
import queue


#===================================
#CONSTANTS
#===================================


#How many datapoints to display on the graph
#20 is pretty realtime but larger values start to lag
NUM_DATAPOINTS = 20

#Which indexes of the input data to display
OUTPUT_CHANNELS = (0,1,2)

#nano is /dev/cu.usbserial-AE01ISIZ
SERIAL_PORT = "/dev/cu.usbserial-AE01ISIZ"

#nano is 9600, teensy is 115200
BAUD_RATE = 9600

OUTPUT_FILE_NAME = "test.csv"

#===================================
#FUNCTIONS
#===================================


def animate(i, dataQueue, plot, timeArray, dataArray):
	currentData = dataQueue.get()

	timeArray.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
	if len(timeArray) > NUM_DATAPOINTS:
		del(timeArray[0])

	dataArray.append(currentData)
	if len(dataArray) > NUM_DATAPOINTS:
		del(dataArray[0])

	numpyArray = np.array(dataArray)
	numpyArray = np.swapaxes(numpyArray, 0, 1)

	plot.clear()

	for i in OUTPUT_CHANNELS:
		plot.plot(timeArray, numpyArray[i])

	plt.tick_params(
		axis='x',          # changes apply to the x-axis
		which='both',      # both major and minor ticks are affected
		bottom=True,      # ticks along the bottom edge are off
 		top=False,         # ticks along the top edge are off
		labelbottom=False)
	plt.xticks(rotation=45, ha='right')
	plt.subplots_adjust(bottom=0.30)
	plt.title('Data over Time')
	plt.ylabel('Data')
	plt.xlabel('Time')


def csvSaveThreadFunc(dataQueue):
	with open(OUTPUT_FILE_NAME, 'w') as outputFile:
		fileWriter = csv.writer(outputFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		while True:
			fileWriter.writerow(dataQueue.get())
			if dataQueue.qsize() > 10:
				print("CAUTION: DataQueue above 10 Entries!")



def serialThreadFunc(dataQueueArray):
	print("SerialThread")
	with serial.Serial(SERIAL_PORT, BAUD_RATE) as ser:
		time.sleep(.5)
		ser.readline()
		while True:
			currentLine = ser.readline().decode("utf-8").strip().split(",")
			currentLine = [float(i) for i in currentLine]
			dataQueueArray.put(currentLine)


#===================================
#MAIN
#===================================


def main():
	dataQueueArray = queue.Queue()

	timeArray = []
	dataArray = []

	fig = plt.figure()
	subplot = fig.add_subplot(1, 1, 1)

	serialThread = threading.Thread(target=serialThreadFunc, args=(dataQueueArray,))
	csvSaveThread = threading.Thread(target=csvSaveThreadFunc, args=(dataQueueArray,))

	serialThread.daemon = True
	serialThread.start()

	csvSaveThread.daemon = True
	csvSaveThread.start()

	animated = animation.FuncAnimation(fig, animate, fargs=(dataQueueArray, subplot, timeArray, dataArray), interval=1)
	plt.show()


if __name__ == "__main__":
	main()



