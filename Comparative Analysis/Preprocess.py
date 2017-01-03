#This file is to preprocess the data of the main file.
import csv
import random
import os.path
from PCA import pca
from CorFil import corFil
from VarFil import varFil

rowdata = []
attr = []
pcadata = []
testpcadata = []
labeldata = []
labeldata_1 = []
file_size=[]
testdata = []
test_file = "test-data.csv"
pca_file = "processed-data.csv"
test_pca_file = "test-data-pca.csv"
input_xtrain = "X_train.txt"
input_xtest = "X_test.txt"


pca_data = "pca.csv"
test_pca_data = "test-pca.csv"


input_ytrain = "y_train.txt"
input_ytest = "y_test.txt"



inter_pca_train = "pcaTrain.csv"
inter_pca_test = "pcaTest.csv"
inter_cor_train = "correlationTrain.csv"
inter_cor_test = "correlationTest.csv"
inter_var_train = "varianceTrain.csv"
inter_var_test = "varianceTest.csv"
inter_withoutreduction = "withoutreduction.csv"



final_pca_train = "pcaTrainFinal.csv"
final_pca_test = "pcaTestFinal.csv"
final_cor_train = "correlationTrainFinal.csv"
final_cor_test = "correlationTestFinal.csv"
final_var_train = "varianceTrainFinal.csv"
final_var_test = "varianceTestFinal.csv"
final_withoutreduction = "withoutreductionFinal.csv"
final_wor_test = "without_red_test.csv"


processed_pca_train = "finalPCATrain.csv"
processed_pca_test = "finalPCATest.csv"
processed_cor_train = "finalCorTrain.csv"
processed_cor_test = "finalCorTest.csv"
processed_var_train = "finalVarTrain.csv"
processed_var_test = "finalVarTest.csv"


def openfile(opt1, opt2):
    if opt1 == 1 and opt2 == 1:
        with open(input_xtrain,"r") as f:
            reader = csv.reader(f, dialect='excel', delimiter=' ')
            for row in reader:
                rowdata.append(row)
        f.close()
    elif opt1 == 2 and opt2 == 1:
        with open(inter_pca_train, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                pcadata.append(row)
        csvfile.close()
    elif opt1 == 3 and opt2 == 1:
        with open(input_xtest,"r") as f:
            reader = csv.reader(f, dialect='excel', delimiter=' ')
            for row in reader:
                testdata.append(row)
        f.close()
    elif opt1 == 4 and opt2 == 1:
        with open(inter_pca_test, 'r') as csvfile:
             lines = csv.reader(csvfile, delimiter=',')
             for row in lines:
                 testpcadata.append(row)
        csvfile.close()
    elif opt1 == 2 and opt2 == 2:
        with open(inter_cor_train, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                pcadata.append(row)
        csvfile.close()
    elif opt1 == 3 and opt2 == 2:
        with open(input_xtest,"r") as f:
            reader = csv.reader(f, dialect='excel', delimiter=' ')
            for row in reader:
                testdata.append(row)
        f.close()
    elif opt1 == 4 and opt2 == 2:
        with open(inter_cor_test, 'r') as csvfile:
             lines = csv.reader(csvfile, delimiter=',')
             for row in lines:
                 testpcadata.append(row)
        csvfile.close()
    elif opt1 == 2 and opt2 == 3:
        with open(inter_var_train, 'r') as csvfile:
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                pcadata.append(row)
        csvfile.close()
    elif opt1 == 3 and opt2 == 3:
        with open(input_xtest,"r") as f:
            reader = csv.reader(f, dialect='excel', delimiter=' ')
            for row in reader:
                testdata.append(row)
        f.close()
    elif opt1 == 4 and opt2 == 3:
        with open(inter_var_test, 'r') as csvfile:
             lines = csv.reader(csvfile, delimiter=',')
             for row in lines:
                 testpcadata.append(row)
        csvfile.close()


def open_label_file(labelOpt):
    if labelOpt == 1:
        with open(input_ytrain,"r") as f:
            reader = csv.reader(f, dialect='excel', delimiter=' ')
            for row in reader:
                labeldata.append(row)
        f.close()
    else:
        with open(input_ytest,"r") as f:
            reader = csv.reader(f, dialect='excel', delimiter=' ')
            for row in reader:
                labeldata_1.append(row)
        f.close()

def strip_empty_chars(stpOpt):
    if stpOpt == 1:
        for i in range(len(rowdata)):
            for j in rowdata[i]:
                if j == '' or j == "" or j ==' ':
                    rowdata[i].remove(j)

        for i in range(len(rowdata)):
            for j in rowdata[i]:
                if j == "":
                    rowdata[i].remove(j)
    else:
        for i in range(len(testdata)):
            for j in testdata[i]:
                if j == '' or j == "" or j ==' ':
                    testdata[i].remove(j)

        for i in range(len(testdata)):
            for j in testdata[i]:
                if j == "":
                    testdata[i].remove(j)

def convert_to_float(conOpt):
    if conOpt == 1:
        for i in range(len(rowdata)):
            for j in range(len(rowdata[i])):
                rowdata[i][j] = float(rowdata[i][j])
            #rowdata[i].append(int(labeldata[i][0]))
    elif conOpt == 2:
        for i in range(len(pcadata)):
            for j in range(len(pcadata[i])):
                pcadata[i][j] = float(pcadata[i][j])
    elif conOpt == 3:
        for i in range(len(testdata)):
            for j in range(len(testdata[i])):
                testdata[i][j] = float(testdata[i][j])
    else:
        for i in range(len(testpcadata)):
            for j in range(len(testpcadata[i])):
                testpcadata[i][j] = float(testpcadata[i][j])

def appendFile(apOpt):
    if apOpt == 1:
        for i in range(len(pcadata)):
            pcadata[i].append(int(labeldata[i][0]))
    else:
        for i in range(len(testpcadata)):
            testpcadata[i].append(float(labeldata_1[i][0]))

def appendfile_woreduction(opt):
    if opt == 1:
        for i in range(len(rowdata)):
            rowdata[i].append(int(labeldata[i][0]))

def appendfile_test(opt):
    if opt == 1:
        for i in range(len(testdata)):
            testdata[i].append(int(labeldata_1[i][0]))

def write_to_new_file(opt1):
    if opt1 == 1:
        if os.path.isfile(final_pca_test) != True:
            with open(final_pca_test, 'w') as f:
                for l in testpcadata:
                    l = str(l).replace('[','')
                    l = l.replace(']','')
                    f.writelines("%s\n" %l )
            f.close()
    elif opt1 == 2:
        if os.path.isfile(final_cor_test) != True:
            with open(final_cor_test, 'w') as f:
                for l in testpcadata:
                    l = str(l).replace('[','')
                    l = l.replace(']','')
                    f.writelines("%s\n" %l )
            f.close()
    elif opt1 == 3:
        if os.path.isfile(final_var_test) != True:
            with open(final_var_test, 'w') as f:
                for l in testpcadata:
                    l = str(l).replace('[','')
                    l = l.replace(']','')
                    f.writelines("%s\n" %l )
            f.close()
    else:
        if os.path.isfile(final_wor_test) != True:
            with open(final_wor_test, 'w') as f:
                for l in testdata:
                    l = str(l).replace('[','')
                    l = l.replace(']','')
                    f.writelines("%s\n" %l )
            f.close()

def write_processed_file(opt):
    if opt == 1:
        if os.path.isfile(final_pca_train) != True:
            with open(final_pca_train, 'wb') as f:
                for l in pcadata:
                    l = str(l).replace('[','')
                    l = l.replace(']','')
                    f.writelines("%s\n" %l )
            f.close()
    elif opt == 2:
        if os.path.isfile(final_cor_train) != True:
            with open(final_cor_train, 'wb') as f:
                for l in pcadata:
                    l = str(l).replace('[','')
                    l = l.replace(']','')
                    f.writelines("%s\n" %l )
            f.close()
    elif opt == 3:
        if os.path.isfile(final_var_train) != True:
            with open(final_var_train, 'wb') as f:
                for l in pcadata:
                    l = str(l).replace('[','')
                    l = l.replace(']','')
                    f.writelines("%s\n" %l )
            f.close()
    else:
        if os.path.isfile(final_withoutreduction) != True:
            with open(final_withoutreduction, 'wb') as f:
                for l in rowdata:
                    l = str(l).replace('[','')
                    l = l.replace(']','')
                    f.writelines("%s\n" %l )
            f.close()



def call(options):
    if options == 1:
        openfile(1,1)
        strip_empty_chars(1)
        convert_to_float(1)
        pca(rowdata,1)
        openfile(2,1)
        open_label_file(1)
        appendFile(1)
        convert_to_float(2)
        write_processed_file(1)
        openfile(3,1)
        strip_empty_chars(2)
        convert_to_float(3)
        pca(testdata,2)
        openfile(4,1)
        open_label_file(2)
        appendFile(2)
        convert_to_float(4)
        write_to_new_file(1)
    elif options == 2:
        openfile(1,1)
        strip_empty_chars(1)
        convert_to_float(1)
        corFil(rowdata,1,attr)
        openfile(2,2)
        open_label_file(1)
        appendFile(1)
        convert_to_float(2)
        write_processed_file(2)
        openfile(3,2)
        strip_empty_chars(2)
        convert_to_float(3)
        corFil(testdata,2,attr)
        openfile(4,2)
        open_label_file(2)
        appendFile(2)
        convert_to_float(4)
        write_to_new_file(2)
    elif options == 3:
        openfile(1,1)
        strip_empty_chars(1)
        convert_to_float(1)
        varFil(rowdata,1,attr)
        openfile(2,3)
        open_label_file(1)
        appendFile(1)
        convert_to_float(2)
        write_processed_file(3)
        openfile(3,3)
        strip_empty_chars(2)
        convert_to_float(3)
        varFil(testdata,2,attr)
        openfile(4,3)
        open_label_file(2)
        appendFile(2)
        convert_to_float(4)
        write_to_new_file(3)
    else:
        openfile(1,1)
        strip_empty_chars(1)
        convert_to_float(1)
        open_label_file(1)
        open_label_file(2)
        appendfile_woreduction(1)
        convert_to_float(1)
        write_processed_file(4)
        openfile(3,1)
        strip_empty_chars(2)
        convert_to_float(3)
        appendfile_test(1)
        convert_to_float(3)
        write_to_new_file(4)

