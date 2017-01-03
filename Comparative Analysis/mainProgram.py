
from Preprocess import call
from knn import knn
from naivebayes import main_def
from dtree import decisionTree

if __name__=="__main__":
    raw = raw_input("Data reduction technique? \n1. PCA 2. Correlation filter 3. Variance Filter 4. Without Reduction\n")
    call(int(raw))
    alg = raw_input("Algorithm for classification? \n1. KNN 2.Naive-Bayes 3.Decision Tree\n")
    if int(alg) == 1:
        knn(raw)
    elif int(alg) == 2:
        main_def(int(raw))
    else:
        decisionTree(int(raw))
