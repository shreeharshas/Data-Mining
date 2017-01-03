#This code is written by Supreeth for the purpose of final project in CSCI B-565

from __future__ import division
import csv
import math
import random

data_set = []
data_set1 = []

def open_file(opt):
    if opt == 1:
        filename = "pcaTrainFinal.csv"
    elif opt == 2:
        filename = "correlationTrainFinal.csv"
    elif opt == 3:
        filename = "varianceTrainFinal.csv"
    else:
        filename = "withoutreductionFinal.csv"

    with open(filename, 'r') as f:
        tot_data = csv.reader(f, delimiter=',')
        for each_row in tot_data:
            data_set.append(each_row)
    f.close()

    for i in range(len(data_set)):
        for j in range(len(data_set[i])):
            data_set[i][j] = float(data_set[i][j])

def open_test_file(opt):
    if opt == 1:
        filename = "pcaTestFinal.csv"
    elif opt == 2:
        filename = "correlationTestFinal.csv"
    elif opt == 3:
        filename = "varianceTestFinal.csv"
    else:
        filename = "without_red_test.csv"
    with open(filename, 'r') as f:
        tot_data = csv.reader(f, delimiter=',')
        for each_row in tot_data:
            data_set1.append(each_row)
    f.close()

def differentiate_data():
    random_indices = []
    training_set = []
    test_set = []
    for i in range(len(data_set)):
        random_indices.append(i)
    random.shuffle(random_indices)
    #len_of_training = 1.0 * len(data_set)
    for i in range(len(data_set)):
        training_set.append(data_set[i])
    for j in range(len(data_set1)):
        test_set.append(data_set1[j])
    return training_set, test_set

#Prepare the model the last column would give us the class
def find_class(train_data):
    separate_classes = {}
    for i in range(len(train_data)):
        each_line = train_data[i]
        if (each_line[-1] not in separate_classes):
            separate_classes[each_line[-1]] = []
        separate_classes[each_line[-1]].append(each_line)
    return separate_classes

def summarize(dataset):
    summaries = [(sum(attribute)/float(len(attribute)), standard_dev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries

def summarizeByClass(dataset):
    separated = find_class(dataset)
    summaries = {}
    for classValue, instances in separated.iteritems():
        summaries[classValue] = summarize(instances)
    return summaries

def standard_dev(nos):
    average = sum(nos)/float(len(nos))
    var = sum([pow(x-average,2) for x in nos])/float(len(nos)-1)
    return math.sqrt(var)

def calc_prob(x, mean, standard_dev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(standard_dev,2))))
    return (1 / (math.sqrt(2*math.pi) * standard_dev)) * exponent

def cal_class_prob(dif_classes, each_row):
    probabilities = {}
    for classValue, classSummaries in dif_classes.iteritems():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, standard_dev = classSummaries[i]
            x = each_row[i]
            probabilities[classValue] *= calc_prob(float(x), mean, standard_dev)
    return probabilities

def predict(dif_classes, each_row):
    probabilities = cal_class_prob(dif_classes, each_row)
    best_label = "nothing"
    best_prob = -1
    for classValue, probability in probabilities.iteritems():
        if best_label is "nothing" or probability > best_prob:
            best_prob = probability
            best_label = classValue
    return best_label

def get_prediction(dif_class, testset):
    final_pred = []
    for i in range(len(testset)):
        result = predict(dif_class, testset[i])
        final_pred.append(result)
    return final_pred

def calc_accuracy(test_set, final_predictions):
    true_positive = 0
    false_negative = 0
    guess = 0
    false_positive = 0
    true_negative = 0
    prediction_dict = {}
    for ctr in range(1,7):
        for ctr1 in range(len(final_predictions)):
            if (ctr not in prediction_dict):
                prediction_dict[ctr] = []
            else:
                if final_predictions[ctr1] == float(ctr):
                    prediction_dict[ctr].append(final_predictions[ctr1])
    length = 0
    for ctr in range(1,7):
        if length < len(prediction_dict[ctr]):
            length = len(prediction_dict[ctr])
            max_lenindict = ctr

    for i in range(len(test_set)):
        if float(test_set[i][-1]) == final_predictions[i]:
            true_positive += 1
            true_negative += 1
        else:
            false_negative+=1
            false_positive += 1
    '''
    for i in range(len(test_set)):
        if float(test_set[i][-1]) == float(max_lenindict):
            guess += 1
    '''
    print "The Accuracy of Naive Bayes Classifier is %.2f" % round((true_positive/float(len(test_set))) * 100.0,2)
    #print "The Accuracy of Naive Bayes Classifier + Guess is %.2f" % round(((right_pred + guess)/float(len(test_set))) * 100.0,2)

    calc_TPR_FPR(true_positive,false_negative, false_positive, true_negative)

def calc_TPR_FPR(TP, FN, FP, TN):
    #print TP, FN
    TPR = TP / (TP + FN)
    FPR = FP / (FP + TN)
    #print "TPR " + str(TPR)
    #print "FPR " + str(FPR)

def predicted_write(arr, opt):
    if opt == 1:
        filename = "pca_predicted.txt"
    elif opt == 2:
        filename = "cor_predicted.txt"
    elif opt == 3:
        filename = "var_predicted.txt"
    else:
        filename = "noreduction_predicted.txt"
    with open(filename, 'wb') as f:
            for each_item in arr:
                each_item = int(each_item)
                f.write("%s\n" %each_item)
    f.close()

def main_def(option):
    open_file(option)
    open_test_file(option)
    train_set, test_set = differentiate_data()
    classes = summarizeByClass(train_set)
    final_predictions = get_prediction(classes, test_set)
    predicted_write(final_predictions, option)
    calc_accuracy(test_set, final_predictions)

