__author__ = 'raghuveer'

import csv
import numpy as np
import matplotlib.pyplot as pl
from collections import defaultdict

def pca(filename, option):
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


    mX = X - np.mean( X, axis=0 )

    cvr = np.cov(mX.T)

    eigenvalue, eigenvector = np.linalg.eig(cvr)

    srt = np.argsort( eigenvalue )[::-1]
    eigenvector = np.matrix( eigenvector[:,srt] )
    eigenvalue = eigenvalue[srt]

    pl.semilogy(eigenvalue.real, '-o')
    pl.title("Log plot of eigen vaue")
    pl.xlabel("Eigen value index")
    pl.ylabel("Eigen value label")
    pl.grid() ; pl.savefig("eigen.png", fmt="png", dpi=200)

    ncomp = 400

    fv = eigenvector[: , :ncomp]

    td = fv.T * mX.T
    td = td.T
    m, n = td.shape

    td = np.array(td.tolist())

    mat = [[0 for y in range(ncomp)]for x in range(M)]
    for i in range(M):
        for j in range(ncomp):
            r = td[i][j]
            mat[i][j] = r.real



    if option == 1:
        with open('pcaTrain.csv','w') as fp:
            a = csv.writer(fp,delimiter = ',')
            a.writerows(mat)
    elif option == 2:
        with open('pcaTest.csv','w') as fp:
            a = csv.writer(fp,delimiter = ',')
            a.writerows(mat)