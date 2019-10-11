#PYTHON 3

import numpy as np
import math
import random
import csv
import matplotlib.pyplot as plt
import time
import serial

def findNextBlank(line, index):
	for i in range(index, len(line)):
		if line[i] == "\t":
			return i
	return -1

def main():
	data = []
	with serial.Serial('/dev/ttys001', 115200, timeout=1) as ser:
		line = ser.readline().decode("utf-8").strip()
		tabs = 1
		for char in line[:len(line)-1]:
			if (char == "\t"):
				tabs += 1
				data.append([])
		print(tabs)
		print(line)
		print(data)
		time.sleep(.001)
		while(True):
			line = ser.readline().decode("utf-8").strip()
			lastblank = 0
			currentblank = findNextBlank(line, 0)
			data[0].append(line[lastblank:currentblank])
			lastblank = currentblank
			currentblank = findNextBlank(line, lastblank+1)

			for i in range (1, tabs-1):
				data[i].append(line[lastblank+1:currentblank])
				lastblank = currentblank
				currentblank = findNextBlank(line, lastblank+1)

			print(data[3])
			time.sleep(.001)


if __name__ == "__main__":
	main()

