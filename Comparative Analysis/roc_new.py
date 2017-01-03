__author__ = 'raghuveer'



import csv
#from sklearn.datasets import make_classification
#from sklearn.linear_model import LogisticRegression
#from sklearn import metrics
#import pandas as pd
#import matplotlib.pyplot as plt
#from ggplot import *
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np
from scipy import interp

#import random


Xtrain = []
ytrain = []
Xtest = []
ytest = []
pred = []
prediction = []
actual = []

# Import some data to play with
with open('correlationTrainFinal.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        row = map(float, row)
        Xtrain.append(row[:-1])
    csvfile.close()

with open('correlationTestFinal.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        row = map(float, row)
        Xtest.append(row[:-1])
    csvfile.close()

with open('y_train.txt', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        row = map(int, row)
        ytrain.append(row)
    csvfile.close()

with open('y_test.txt', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        row = map(int, row)
        ytest.append(row)
    csvfile.close()


with open('predictionCor.csv', 'r') as csvfile:
    lines = csv.reader(csvfile, delimiter=',')
    for row in lines:
        row = map(float, row)
        pred.append(row)
    csvfile.close()


for i in range(len(pred)):
    x = ytest[i]
    y = pred[i]
    if int(x[0]) == int(y[0]):
        prediction.append(float(1))
    else:
        prediction.append(float(0))

for j in range(len(pred)):
    x = ytest[j]
    actual.append(float(x[0]))

actual = label_binarize(actual, classes=[1,2,3,4,5,6])
prediction = label_binarize(prediction, classes=[1,2,3,4,5,6])
n_classes = actual.shape[1]

#print prediction
#print actual#
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(actual[:, i], prediction[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

#fpr, tpr, thr = roc_curve(actual,prediction)
#area = auc(fpr, tpr)



fpr["micro"], tpr["micro"], _ = roc_curve(actual.ravel(), prediction.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])


##############################################################################
# Plot of a ROC curve for a specific class
plt.figure()
plt.plot(fpr[2], tpr[2], label='ROC curve (area = %0.2f)' % roc_auc[2])
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()


##############################################################################
# Plot ROC curves for the multiclass problem

# Compute macro-average ROC curve and ROC area

# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += interp(all_fpr, fpr[i], tpr[i])

# Finally average it and compute AUC
mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Plot all ROC curves
plt.figure()
plt.plot(fpr["micro"], tpr["micro"],
         label='micro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["micro"]),
         linewidth=2)

plt.plot(fpr["macro"], tpr["macro"],
         label='macro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         linewidth=2)

for i in range(n_classes):
    plt.plot(fpr[i], tpr[i], label='ROC curve of class {0} (area = {1:0.2f})'
                                   ''.format(i, roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Some extension of Receiver operating characteristic to multi-class')
plt.legend(loc="lower right")
plt.show()





'''
plt.title('Receiver Operating Characteristic')
plt.plot(fpr, tpr, 'b',
label='AUC = %0.2f'% area)
plt.legend(loc='lower right')
plt.plot([0,1],[0,1],'r--')
plt.xlim([-0.1,1.2])
plt.ylim([-0.1,1.2])
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.show()
'''
#clf = LogisticRegression()
#clf.fit(Xtrain, ytrain)

#preds = clf.predict_proba(Xtest)[:,1]
#fpr, tpr, _ = metrics.roc_curve(ytest, preds)

#plt.plot(fpr,tpr)

#plt.show()