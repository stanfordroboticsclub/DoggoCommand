#ONLY PYTHON 2 NERDS

import numpy as np
import math
import random
import csv
import matplotlib.pyplot as plt
import time

def loadCsvData(fileName):
	matrix = []
	empty = False
	with open(fileName) as f:
		reader = csv.reader(f)
		for row in reader:
			doubleRow = []
			for value in row:
				# filters out all lines with empty data
				if value == "":
					empty = True
				doubleRow.append(value)
			if empty == False:
				matrix.append(doubleRow)
			empty = False
	return np.asarray(matrix)

def translateDataShape(inputData):
	matrix = np.zeros(shape=(np.shape(inputData)[1], np.shape(inputData)[0]-1))
	for i in range (0, np.shape(inputData)[1]):
		for j in range (1, np.shape(inputData)[0]):
			matrix[i][j-1] = inputData[j][i]
	nameMatrix = []
	for i in range(0, np.shape(inputData)[1]):
		nameMatrix.append(inputData[0][i])

	return np.asarray(matrix), nameMatrix

def easyPlot(data, nameData, indexs):
	plotArray = []
	for i in indexs:
		plt.plot(data[i], label=nameData[i])		
	plt.legend()

def main():
	print(".CSV is assumed to have the names in the top row")
	inputData = loadCsvData(raw_input("Enter a .CSV file to open: "))
	fixedData, nameData = translateDataShape(inputData)

	print ("Common Presents: EstTheta = (1, 5, 9, 13), EstGamma = (3, 7, 11, 15)")
	easyPlot(fixedData, nameData, input("Please enter a tuple of the indexes to show: "))
	plt.show()

if __name__ == "__main__":
	main()

