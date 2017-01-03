__author__ = 'raghuveer'


import numpy as np
import csv
import scipy
from scipy.stats.stats import pearsonr
from collections import defaultdict

def varFil(filename, option, attr):
    X = np.array([[j for j in i] for i in filename])
    M, N = X.shape

    cor = defaultdict(list)

    mini = 1000000
    maxi = 0

    for x in range(M):
        for y in range(N):
            if X[x][y] < mini:
                mini = X[x][y]
            if X[x][y] > maxi:
                maxi = X[x][y]

    if option == 1:
        for p in range(N):
            numpyArrayA = np.array(X[:,p])
            b = np.var(numpyArrayA)
            if b < 0.05:
                attr.append(p)






    attr = sorted(attr, key=None, reverse=True)

    for i in attr:
        X = np.delete(X,i,1)



    if option == 1:
        with open('varianceTrain.csv','w') as fp:
            a = csv.writer(fp,delimiter = ',')
            a.writerows(X)
    elif option == 2:
        with open('varianceTest.csv','w') as fp:
            a = csv.writer(fp,delimiter = ',')
            a.writerows(X)