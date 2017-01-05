import math
import operator
from pprint import pprint

'''
Decision tree classifier
Created two classes - SimpleNode to hold the node information of the decision tree
                      dataHolder to contain the dataset and also metadata such as entropy and list of information gains

Visualizing the decision tree:
I have created the decision tree with nodes which can contain one of these three:a feature, a feature's value or a class

The rule matrix is as follows:
The node of type indicated on the left column can have child nodes of the type indicated horizontally

                        feature    value    class
                       ---------------------------
              feature |              x
              value   |    x                  x
              class   |

                      Sample decision tree is as follows:

                                   feature 2     (root is always a feature)
                                   /      \
                                  /        \
                           value1         value2   (these can be only values of the parent feature)
                            /  \          /    \
                          /     \        /      \
                    feature3   class   feature1  feature5  (value node points to a single child which is either a feature or a class
                      /   \              /  |  \       |
                     /     \            /   |   \      |
             value1     value2     value1   |  value3  value1
                  |        |         /    value2 |       |
                  |        |        /       |    |       |
                class1    class2  feature4  |    class3  class1  (leaf is always a class)
                                      |     |
                                      |     class2
                                     value1
                                      |
                                      |
                                     class2
'''
def findSatisfyingChild(node, value):
    for child in node.children:
        if child.name == value:
            return child
    return None

def classify(datarow, node):
    #for datarow in dataset:
    if True:
        if node is not None:
            if node.nodetype == "feature":
                children = node.children
                if children is not None:
                    s_child = findSatisfyingChild(node, datarow[node.name])
                    if s_child is None:
                        # s_child.associated_dataholder.CalculateNumbers()
                        node.associated_dataholder.CalculateWhatIsNeededForEntropy()
                        return node.associated_dataholder.getMajorityClass()
                    else:
                        # do stuff similar to value condition
                        feature_or_class_node = s_child.children[0]
                        if feature_or_class_node.nodetype == "feature":
                            return classify(datarow, feature_or_class_node)
                        else:
                            return feature_or_class_node

            elif node.nodetype == "value":
                    feature_or_class_node = node.children[0]
                    '''value = datarow[feature_node.name]
                    c = node.getChildren(node)'''
                    if feature_or_class_node.nodetype == "feature":
                        return classify(datarow, feature_or_class_node)
                    else:
                        return node
            else:
                return node
        # checking part end

#def binary_vectorize(datatset):

#    return bv_dataset

def getNonNumericFeatures(datarow):# returns a dictionary of features with indication of whether they are numeric or not
    featureType = dict()
    for i in range(datarow):
        if isinstance(datarow[i], int) == False or isinstance(datarow[i], float) == False:
            featureType[i] = False
        else:
            featureType[i] = True
    return featureType

def BinaryVectorize(dataset, feature):          # optional check - to be implemented if necessary
    for isNotNumeric in getNonNumericFeatures(dataset[0]):
        pass
    pass

def isContinuous(dataset, feature):
    single_feature_values_list = list()
    for datarow in dataset:
        if datarow[feature] not in single_feature_values_list:
            single_feature_values_list.append(datarow[feature])

    if float(len(single_feature_values_list))/len(dataset) >= 0.7:
        return True
    else:
        return False

def discretize(dataset, features):
    ''' for datarow in dataset:
         for every feature of the dataset
             find feature's min and max values
             for every value of datarow[feature]
             if max != min
                 value = (value-min)/(max-min)
             else
                 value = value itself'''
    for datarow in dataset:
        list_feature_values = list()
        for feature in features:
            list_feature_values.append(datarow[feature])

        min_of_f_column = min(list_feature_values)
        max_of_f_column = max(list_feature_values)

        numer = datarow[feature] - min_of_f_column
        denom = max_of_f_column - min_of_f_column

        if denom != 0:
            datarow[feature] = numer/denom

class SimpleNode:
    '''name
	children
	nodetype
	associated_dataholder
	'''

    def __init__(self):
        self.name = None
        self.nodetype = None
        self.children = None
        self.associated_dataholder = None

    def createNode(self, name, nodetype, children=None, associated_dataholder=None):
        self.name = name
        self.nodetype = nodetype
        self.children = children
        self.associated_dataholder = associated_dataholder

    def addChild(self, childname, childtype=None):
        if self.children is None:
            self.children = list()
        if isinstance(childname, SimpleNode):
            self.children.append(childname)
        else:
            ch = SimpleNode()
            ch.createNode(childname, "default")
            self.children.append(ch)

    def getNode(self):
        return self

# for every node, print its value and its children's value separated by an arrow

def print_node(ch):
    if ch is not None:
        print ch.nodetype, ch.name
        if ch.children is not None:
            for child in ch.children:
                #print ch.nodetype, child.name
                print_node(child)


def getCounts(dataset, uniq_class, num_feat):
    count = 0
    for datarow in dataset:
        if datarow[num_feat-1] == uniq_class:
            count += 1
    return count

def get_unique_feature_values_dict(dataset, input_feature):
    uniqueList = list()
    for datarow in dataset:
        if datarow[input_feature] not in uniqueList:
            uniqueList.append(datarow[input_feature])
    return uniqueList

def get_entropy(dataset, features_not_to_use=None):
    e_of_s = 0.0
    sizeofds = len(dataset)
    if sizeofds > 0:
        n_of_feat = len(dataset[0])
        denominator = sizeofds
        uniqLst = get_unique_feature_values_dict(dataset, n_of_feat-1)
        for uniq_class in uniqLst:   # last feature is the class
            numerator = getCounts(dataset, uniq_class, n_of_feat)
            p = float(numerator)/denominator
            if p > 0:
                minus_p = -1 * p
                lg_p = math.log(p, 2)
                e_of_s += minus_p * lg_p  # greater than one but less than log(len(unique_classes) to base 2)
    return e_of_s

class dataHolder:
    '''dataset							# __init__
	IsPure							# getPureClass
	classes							# calc_class_list
	features_list					# calc_feature_list
	feature_uniqueValues			# calc_unique_feature_values
	entropy 						# calc_entropy
	info_gain_features_map			# calc_gain
	best_feature					# calc_best_feature
	class_counts					# calc_class_counts
	number_of_features				# setNumberofFeatures
	entropy							# calc_entropy
	#features_to_exclude				#
	'''
    ''' make sure all the above values have been initialized'''

    def __init__(self, dataset, excluded_features=None):
        self.dataset = dataset
        self.featurestoexclude = excluded_features
        self.removeFeatures(excluded_features)
        self.len_dataset = None
        self.IsPure = None  # getPureClass
        self.classes = None  # calc_class_list
        self.features_list = None  # calc_feature_list
        self.feature_uniqueValues = None  # calc_unique_feature_values
        self.entropy = None  # calc_entropy
        self.info_gain_features_map = None  # calc_gain
        self.best_feature = None  # calc_best_feature
        self.class_counts = None  # calc_class_counts
        self.number_of_features = None  # setNumberofFeatures
        self.entropy = None

    def setLengthOfDS(self):
        if self.dataset is None:
            self.len_dataset = 0
        elif len(self.dataset) == 0:
            self.len_dataset = 0
        else:
            self.len_dataset = len(self.dataset)

    def setNumberofFeatures(self):
        if self.dataset is None:
            self.number_of_features = 0
        elif len(self.dataset) ==0:
            self.number_of_features = 0
        else:
            self.number_of_features = len(self.dataset[0])

    def calc_feature_list(self):
        if self.len_dataset > 0:
            if self.features_list is None:
                self.features_list = list()
            for i in range(0, len(self.dataset[0])):
                if i not in self.features_list:
                    self.features_list.append(i)

    def calc_class_list(self):
        if self.classes is None:
            self.classes = list()
        for datarow in self.dataset:
            self.classes.append(datarow[self.number_of_features - 1])

    def calcclassCounts(self):
        if self.len_dataset > 0:
            count = 0
            if self.class_counts is None:
                self.class_counts = dict()
            for uniq_class in self.feature_uniqueValues[self.number_of_features-1]:
                for i in range(0, len(self.dataset)):
                    if self.dataset[i][self.number_of_features - 1] == uniq_class:
                        count += 1
                self.class_counts[uniq_class] = count

    def calc_unique_feature_values(self):
        if self.len_dataset > 0:
            for feat in self.features_list:
                if feat not in self.featurestoexclude:
                    u_list = list()
                    for datarow in self.dataset:
                        val = datarow[feat]
                        if val not in u_list:
                            u_list.append(val)
                    if self.feature_uniqueValues is None:
                        self.feature_uniqueValues = dict()
                    self.feature_uniqueValues[feat] = u_list

    def getPureClass(self):
        temp_class_list = list()
        for datarow in self.dataset:
            temp_class_name = datarow[self.number_of_features - 1]
            if temp_class_name not in temp_class_list:
                temp_class_list.append(temp_class_name)
        if len(temp_class_list) == 1:
            self.IsPure = True
            return temp_class_list[0]
        else:
            self.IsPure = False

    def getMajorityClass(self):
        if self.len_dataset > 0:
            return max(self.class_counts.iteritems(), key=operator.itemgetter(1))[0]

    def setMajorityClass(self):
        for clas in self.classes:
            clas_counter = 0
            for datarow in self.dataset:
                if datarow[self.number_of_features - 1] == clas:
                    clas_counter += 1
            self.class_counts[clas] = clas_counter

    def IsEmpty(self):
        if self.dataset is None:
            return True
        else:
            if len(self.dataset) == 0:
                return True
        return False

    def split(self, feature_name, value):
        retDataset = list()
        for datarow in self.dataset:
            if datarow[feature_name] == value:
                retDataset.append(datarow)
        return retDataset

    def hasFeatures(self):
        if self.features_list is None:
            return False
        elif len(self.features_list) == 0:
            return False
        return True

    def calc_entropy(self):
        self.setLengthOfDS()
        self.setNumberofFeatures()
        self.calc_feature_list()
        # self.removeFeatures()
        self.calc_unique_feature_values()
        self.calcclassCounts()
        self.calc_class_list()
        self.setMajorityClass()
        self.getPureClass()
        # E(S) = sigma(-p log(p)) where p is the ratio of number of examples of particular class to total number of examples
        if self.len_dataset > 0:
            e_of_s = 0.0
            denominator = len(self.dataset)
            for uniq_class in self.feature_uniqueValues[self.number_of_features - 1]:  # last feature is the class
                numerator = self.class_counts[uniq_class]
                p = float(numerator) / denominator
                if p > 0:
                    minus_p = -1 * p
                    lg_p = math.log(p, 2)
                    e_of_s += minus_p * lg_p  # greater than one but less than log(len(unique_classes) to base 2)
            # print "entropy of dataset:\n" + str(dataset) + "\nis:" + str(e_of_s)
            self.entropy = e_of_s

    def getSubset(self, value_f, feature):
        tempList = list()
        for datarow in self.dataset:
            if datarow[feature] == value_f:
                tempList.append(datarow)
        return tempList

    def set_gains(self, inp_feature):
        sum_of_entropies_weighted_by_proportion = 0
        s_dataset = len(self.dataset)
        for unique_feature_value in self.feature_uniqueValues[inp_feature]:
            temp_newds = self.getSubset(unique_feature_value, inp_feature)
            s_newds = len(temp_newds)

            if s_newds == 0:
                e_of_newds = 0.0
                proportion = 0
            else:
                proportion = float(s_newds) / s_dataset
                e_of_newds = get_entropy(temp_newds)
            sum_of_entropies_weighted_by_proportion += proportion * e_of_newds
        infogain = self.entropy - sum_of_entropies_weighted_by_proportion
        return infogain

    def calc_gain(self):
        self.setLengthOfDS()
        self.setNumberofFeatures()
        self.calc_feature_list()
        self.calc_unique_feature_values()
        self.calcclassCounts()
        self.calc_class_list()
        self.setMajorityClass()
        self.getPureClass()
        self.calc_entropy()

        if self.len_dataset > 0:
            if self.info_gain_features_map is None:
                self.info_gain_features_map = dict()
            for feature_name in self.features_list:
                if feature_name not in self.featurestoexclude and feature_name!= self.number_of_features-1:
                    self.info_gain_features_map[feature_name] = self.set_gains(feature_name)

    def calc_best_feature(self):
        if self.len_dataset > 0:
            self.best_feature = max(self.info_gain_features_map.iteritems(), key=operator.itemgetter(1))[0]

    def calc_gini(self):
        pass

    def removeFeatures(self, features_to_remove):
        '''if features_to_remove is not None:
            for feature_to_exclude in features_to_remove:
                if feature_to_exclude in self.features_list:
                    self.features_list.remove(feature_to_exclude)'''
        if self.featurestoexclude is None:
            self.featurestoexclude = list()
        if features_to_remove is not None:
            for fe in features_to_remove:
                if fe not in self.featurestoexclude:
                    self.featurestoexclude.append(fe)

    def CalculateWhatIsNeededForEntropy(self):
        self.calc_entropy()

    def CalculateNumbers(self):
        self.calc_gain()
        self.calc_best_feature()
        self.calc_gini()



def buildtree(nd, dataholder, features_to_exclude=[], default_class=None):
    dataholder.CalculateNumbers()
    if dataholder.IsPure:
        root = SimpleNode()
        root.createNode(dataholder.getPureClass(), "class", None, dataholder)
        return root

    #if dataholder.hasFeatures() == False:
    if len(dataholder.featurestoexclude) == len(dataholder.features_list)-1:
        default_class = dataholder.getMajorityClass()
        root = SimpleNode()
        root.createNode(default_class, "class", None, dataholder)
        return root
    else:
        root = SimpleNode()
        root.createNode(dataholder.best_feature, "feature",None,dataholder)
        for uniq in dataholder.feature_uniqueValues[dataholder.best_feature]:
            new_dholder = dataHolder(dataholder.getSubset(uniq, dataholder.best_feature))
            new_dholder.CalculateNumbers()
            node = SimpleNode()
            node.createNode(uniq, "value", None, new_dholder)

            if new_dholder.IsEmpty():
                node.addChild(dataholder.getMajorityClass(), "class")
            else:
                if features_to_exclude is None:
                    features_to_exclude=list()
                features_to_exclude.append(new_dholder.best_feature)
                new_dholder.removeFeatures(features_to_exclude)
                node.addChild(buildtree(uniq, new_dholder, features_to_exclude, default_class))
            root.addChild(node, None)
    return root


#######################################################################################################################
# main program starts

# START FILE HANDLING CODE #
# start read from iris datafile user lists

print "reading train data..."
#f = open('auto-mpg.data_u', 'r')
#f = open('abalone.data', 'r')
#f = open('auto-mpg.data', 'r')
f = open('zoo.data', 'r')
autompg_data_raw = f.readlines()
f.close()
# end read from autompg datafile user lists
autompg_data = list()
print "finished reading train data\ncleaning data..."
for autompg_datum_raw in autompg_data_raw:
    splitArr = autompg_datum_raw.split('\t')
    tempList = list()
    for j in range(0, len(splitArr)):
        tempList.append(str.strip(splitArr[j]))
    autompg_data.append(tempList)

Dataholder = dataHolder(autompg_data)
print "finished cleaning data\nBuilding tree..."
node = buildtree(None, Dataholder, None, None)

print "built tree\nreading test data..."
#print_node(node)
# main program ends
#######################################################################################################################
# validation begins

datast = list()

'''# abalone.data
#positive criteria  (part of dataset)
datast.append(["0.365", "0.295", "0.08", "0.2555", "0.097", "0.043", "0.1", "7"])
datast.append(["0.24", "0.175", "0.045", "0.07", "0.0315", "0.0235", "0.02", "5"])
datast.append(["0.205", "0.15", "0.055", "0.042", "0.0255", "0.015", "0.012", "5"])
datast.append(["0.21", "0.15", "0.05", "0.042", "0.0175", "0.0125", "0.015", "4"])
datast.append(["0.39", "0.295", "0.095", "0.203", "0.0875", "0.045", "0.075", "7"])
datast.append(["0.615", "0.48", "0.165", "1.1615", "0.513", "0.301", "0.305", "10"])

#negative criteria (new input dataset)
datast.append(["0.465", "0.295", "0.08", "0.2555", "0.097", "0.043", "0.1", "8"])
'''

'''# auto-mpg.data
# positive test (for data given in training set)
datast.append(["21.6", "4", "121", "115", "2795", "15.7", "78", "2"])
datast.append(["32", "4", "135", "84", "2295", "11.6", "82", "1"])
datast.append(["28", "4", "120", "79", "2625", "18.6", "82", "1"])
datast.append(["31", "4", "119", "82", "2720", "19.4", "82", "1"])
# negative test (for test data)
datast.append(["31", "10", "119", "83", "2720", "19.4", "82", "4"])
'''

f = open('zoo.test', 'r')
autompg_test_raw = f.readlines()
f.close()
# end read from autompg datafile user lists
autompg_test = list()
print "finished reading test data\ncleaning test..."
for autompg_t_item_raw in autompg_test_raw:
    splitTArr = autompg_t_item_raw.split('\t')
    tempTList = list()
    for j in range(0, len(splitTArr)):
        tempTList.append(str.strip(splitTArr[j]))
    autompg_test.append(tempTList)

print "finished reading test\nstarting classification..."
testingNodesList = dict()
classifiedNodesList = dict()
i = 0
for datarow in autompg_test:
    testingNodesList[i] = datarow[len(datarow)-1]
    classifiedNode = classify(datarow, node)
    print datarow,
    if isinstance(classifiedNode, SimpleNode):
        print classifiedNode.name
        classifiedNodesList[i] = classifiedNode.name
    else:
        print classifiedNode
        classifiedNodesList[i] = classifiedNode
    i += 1
print "\nfinished classifying\ncalculating accuracy..."

predictedCorrectValues = 0
for i in range(0, len(testingNodesList)):
    if testingNodesList[i] == classifiedNodesList[i]:
        predictedCorrectValues += 1

accuracy = (float(predictedCorrectValues)/len(testingNodesList)) * 100
print "Found Accuracy:", accuracy, "%"

# validation ends
#######################################################################################################################