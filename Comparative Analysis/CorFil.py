__author__ = 'raghuveer'


import numpy as np
import csv
import scipy
from scipy.stats.stats import pearsonr
from collections import defaultdict

def corFil(filename, option, attr):
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
            for q in range(N):
                if p != q:
                    a, b = pearsonr(X[:,p],X[:,q])
                    if b >= abs(0.98):
                        cor[p].append(q)




        for value in cor.itervalues():
            for i in value:
                if i not in attr:
                    attr.append(i)


    attr = sorted(attr, key=None, reverse=True)

    for i in attr:
        X = np.delete(X,i,1)



    if option == 1:
        with open('correlationTrain.csv','w') as fp:
            a = csv.writer(fp,delimiter = ',')
            a.writerows(X)
    elif option == 2:
        with open('correlationTest.csv','w') as fp:
            a = csv.writer(fp,delimiter = ',')
            a.writerows(X)