import csv
import numpy as np
import random
import matplotlib.pyplot as plt

#K-Means clustering implementation
# Function that computes the distance between data points
def distanceCalc(strList, clustersX, clustersY):
    sqrtAnswer = 0
    
    for i in range(len(strList)):
        answers = []
        for j in range(len(clustersX)):
            temp = np.sqrt((float(strList[i][1]) - float(clustersX[j]))**2 + (float(strList[i][2]) - float(clustersY[j]))**2)
            answers.append(temp)
        
        shortestDistance = min(answers)
        indexOfShortestDistance = answers.index(shortestDistance) + 1
        if len(strList[i]) >= 4:
            strList[i][3] = indexOfShortestDistance
        else:
            strList[i].append(indexOfShortestDistance)

        sqrtAnswer += (shortestDistance** 2)
        
    return strList, sqrtAnswer

# Function that reads data in from the csv files
def readCSV(filename):
    with open(filename, 'r') as csvfile:
        myReader = csv.reader(csvfile, delimiter =',')
        stringList = []
        for row in myReader:
            stringList.append(row)

    # Removes Headings
    stringList.pop(0)
    return stringList

# The initialisation procedure
def initClusters(strList, numClusters):
    pickListX = []
    pickListY = []

    for i in range(len(strList)):
        pickListX.append(strList[i][1])
        pickListY.append(strList[i][2])

    clusterPointsX = random.sample(pickListX, numClusters)
    clusterPointsY = random.sample(pickListY, numClusters)
    # Returns list of x and list of y points, size of list depends of numClusters
    return clusterPointsX, clusterPointsY

# Implementing the k-means algorithm, using appropriate looping
def kMeansAlgo(dataList, x, y, numOfIterations):
    
    # Array of colours, empty space to shift everything by 1 (clusters range from 1 to n)
    cmaps = [" ", "Blue", "Green", "Purple", "Pink", "Red", "Orange", "Brown", "Black", "Yellow", "Grey"] 
    
    dataCalculated = dataList.copy()

    for i in range(numOfIterations):
        dataCalculated, sqrtAnswer = distanceCalc(dataCalculated, x, y)
        for j in range(len(x)):
            count = 0
            answerX = 0
            answerY = 0
            for k in range(len(dataList)):
                if dataCalculated[k][3] == j + 1:
                    count += 1
                    answerX += float(dataCalculated[k][1])
                    answerY += float(dataCalculated[k][2])

            if count > 0:
                x[j] = (answerX / count)
                y[j] = (answerY / count)
        
        print("Convergence: " + str(sqrtAnswer))
        
        
        # Plotting Data Points
        for i in range(len(dataCalculated)):
            plt.scatter(float(dataCalculated[i][1]), float(dataCalculated[i][2]),c=cmaps[dataCalculated[i][3]])

        plt.show()
    
    print("\n")
    # Returns list of data with its cluster assigned
    return dataCalculated
            
# Reading in dataset and asking user which database file he wants to use
dataSet1 = readCSV(input('''Plese enter the file name you want to use: 
                    data1953.csv
                    data2008.csv
                    dataBoth.csv \n''' ))               
                                                                                        
# Initalising cluster points
cluster_amount = int(input("Input cluster amount:"))                     
x, y = initClusters(dataSet1, cluster_amount)

# Starting algorithm
k_cluster = int(input("Enter amout of times algorithm must run:"))
kMean = kMeansAlgo(dataSet1, x, y, k_cluster)

# Print out the results
countryCount = []

for i in range(len(x)):
    countryCount.append(0)
    countryList = []
    meanBirthExpectancy = []
    meanLifeExpectancy = []
    for j in range(len(kMean)):
        if kMean[j][3] == i + 1:
            countryCount[i] += 1
            countryList.append(kMean[j][0])
            meanBirthExpectancy.append(kMean[j][1])
            meanLifeExpectancy.append(kMean[j][2])

    # Printing out results
    print("Number of countries belonging to cluster " + str(i + 1) + ": " + str(countryCount[i]))
    listToStr = ", ".join([str(element) for element in countryList])
    print("List of countries belonging to cluster " + str(i + 1) + ": " + listToStr)
    
    # Working out the means(average)
    meanBirthAdded = 0
    meanLifeAdded = 0
    for k in range(len(meanBirthExpectancy)):
        meanBirthAdded += float(meanBirthExpectancy[k]) 
        meanLifeAdded += float(meanLifeExpectancy[k])
    
    meanBirthAnswer = (meanBirthAdded / len(meanBirthExpectancy))
    meanLifeAnswer = (meanLifeAdded / len(meanLifeExpectancy))
    
    # Outputting the means
    print("The mean birth rate for cluster " + str(i + 1) + ": " + str(meanBirthAnswer))
    print("The mean life expectancy for cluster " + str(i + 1) + ": " + str(meanLifeAnswer))
    print("\n")
