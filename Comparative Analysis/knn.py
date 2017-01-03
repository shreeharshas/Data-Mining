__author__ = 'raghuveer'

import csv
import random
import math
import operator

testResult = []
with open("y_test.txt", 'rb') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        for row in lines:
            row = map(int, row)
            testResult.append(row)
csvfile.close()

def loadDataset(filename, testdata, trainingSet=[] , testSet=[]):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile, delimiter=',')
        train = list(lines)
        for x in range(len(train)):
                trainingSet.append(train[x])
    csvfile.close()

    with open(testdata, 'rb') as csvf:
         lines = csv.reader(csvf, delimiter=',')
         test = list(lines)
         for x in range(len(test)):
            testSet.append(test[x])
    csvf.close()

def dist(instance1, instance2, length):
    d = 0
    for i in range(length):
        d += pow((float(instance1[i]) - float(instance2[i])), 2)
    distance = math.sqrt(d)
    return distance


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
        d = dist(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], d))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
    voting = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in voting:
            voting[response] += 1
        else:
            voting[response] = 1
    sortedNeighbors = sorted(voting.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedNeighbors[0][0]


def getAccuracy(testSet, predictions):

    correct = 0
    count = 0
    for x in range(len(testSet)):
        try:
            if float(testSet[x][-1]) == float(predictions[x]):
                correct += 1
                count += 1
        except:
            print "Parse error"
    return (correct/float(len(testSet))) * 100.0

def knn(option):
    trainingSet=[]
    testSet=[]
    if option == 1:
        loadDataset('pcaTrainFinal.csv', 'pcaTestFinal.csv', trainingSet, testSet)
    elif option == 2:
        loadDataset('correlationTrainFinal.csv', 'correlationTestFinal.csv', trainingSet, testSet)
    elif option == 3:
        loadDataset('varianceTrainFinal.csv', 'varianceTestFinal.csv', trainingSet, testSet)
    else:
        loadDataset('withoutreductionFinal.csv', 'without_red_test.csv', trainingSet, testSet)
    print 'Train set: ' + repr(len(trainingSet))
    print 'Test set: ' + repr(len(testSet))
    k = 6
    predictions=[]
    counter = 0
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        #print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
        counter = counter + 1
    accuracy = getAccuracy(testSet, predictions)
    print 'Accuracy ' + str(accuracy)
    if option == 1:
        with open('predictionPCA.csv', 'wb') as f:
            for l in predictions:
                l = str(l).replace('[','')
                l = l.replace(']','')
                f.writelines("%s\n" %l )
        f.close()
    elif option == 2:
        with open('predictionCor.csv', 'wb') as f:
            for l in predictions:
                l = str(l).replace('[','')
                l = l.replace(']','')
                f.writelines("%s\n" %l )
        f.close()
    elif option == 3:
        with open('predictionVar.csv', 'wb') as f:
            for l in predictions:
                l = str(l).replace('[','')
                l = l.replace(']','')
                f.writelines("%s\n" %l )
        f.close()
    else:
        with open('prediction_nored.csv', 'wb') as f:
            for l in predictions:
                l = str(l).replace('[','')
                l = l.replace(']','')
                f.writelines("%s\n" %l )
        f.close()


