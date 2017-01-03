import math
import operator
from pprint import pprint

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

def normalize(dataset):
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
        for feature in range(0, len(datarow) - 1):
            list_feature_values.append(float(datarow[feature]))

        min_of_f_column = min(list_feature_values)
        max_of_f_column = max(list_feature_values)

        numer = float(datarow[feature]) - min_of_f_column
        denom = max_of_f_column - min_of_f_column

        if denom != 0:
            datarow[feature] = numer/denom

def discretize(dataset):
    list_feature_valus = dict()
    for p in range(0, len(dataset)):
        datarow = dataset[p]
        for feature in range(0, len(datarow)):
            f = float(datarow[feature])

            if feature not in list_feature_valus:
                tempRow = list()
                tempRow.append(f)
                list_feature_valus[feature] = tempRow
            else:
                tempRow = list_feature_valus[feature]
                tempRow.append(f)
                list_feature_valus[feature] = tempRow


    for p in range(0, len(dataset)):
        datarow = dataset[p]
        for feature in range(0, len(datarow) - 1):
            sorted_list = sorted(list_feature_valus[feature])
            lst = sorted_list[::(len(sorted_list))/10]

            print "\rRow number:",p,"of ",len(dataset),

            #avg_of_f_column = sum(list_feature_valus[feature])/len(list_feature_valus[feature])
            #abs_of_value = abs(float(datarow[feature]))

            #if abs_of_value > avg_of_f_column:
                #datarow[feature] = 0.6
            #elif abs_of_value == avg_of_f_column:
                #datarow[feature] = abs_of_value
            #else:
                #datarow[feature] = 0.4

            d_val = float(datarow[feature])
            if d_val >= lst[9]:
                datarow[feature] = 10
            elif d_val >= lst[8] and d_val < lst[9]:
                datarow[feature] = 9
            elif d_val >= lst[7] and d_val < lst[8]:
                datarow[feature] = 8
            elif d_val >= lst[6] and d_val < lst[7]:
                datarow[feature] = 7
            elif d_val >= lst[5] and d_val < lst[6]:
                datarow[feature] = 6
            elif d_val >= lst[4] and d_val < lst[5]:
                datarow[feature] = 5
            elif d_val >= lst[3] and d_val < lst[4]:
                datarow[feature] = 4
            elif d_val >= lst[2] and d_val < lst[3]:
                datarow[feature] = 3
            elif d_val >= lst[1] and d_val < lst[2]:
                datarow[feature] = 2
            elif d_val >= lst[0] and d_val < lst[1]:
                datarow[feature] = 1
            else:
                datarow[feature] = 0


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

def predicted_write(arr, opt):
    if opt == 1:
        filename = "pca_predicted_dt.txt"
    elif opt == 2:
        filename = "cor_predicted_dt.txt"
    elif opt == 3:
        filename = "var_predicted_dt.txt"
    else:
        filename = "noreduction_predicted_dt.txt"
    i = 0
    with open(filename, 'wb') as f:
        for key, val in arr.items():
            val = float(val)
            int_val = int(val)
            f.write("%s\n" %int_val)
    f.close()
#######################################################################################################################
# decision tree program starts

def decisionTree(option):
  # START FILE HANDLING CODE #
  # start read from iris datafile user lists

  print "reading train data..."
  #autompg_data_raw = []
  trainDataSetName = ""
  testDataSetName = ""
  
  if option == 1:  
    trainDataSetName = "pcaTrainFinal.csv"
    testDataSetName = "pcaTestFinal.csv"
  
  elif option == 2:  
    trainDataSetName = "correlationTrainFinal.csv"
    testDataSetName = "correlationTestFinal.csv"
    
  elif option == 3:
    trainDataSetName = "varianceTrainFinal.csv"
    testDataSetName = "varianceTestFinal.csv"

  else:
    trainDataSetName = "withoutreductionFinal.csv"
    testDataSetName = "without_red_test.csv"
  '''
  with open(trainDataSetName, 'r') as f:
        tot_data = csv.reader(f, delimiter=',')
        for each_row in tot_data:
            autompg_data_raw.append(each_row)
  f.close()
  '''
  f = open(trainDataSetName, 'r')
  autompg_data_raw = f.readlines()
  f.close()
  # end read from autompg datafile user lists
  autompg_data = list()
  print "finished reading train data\ncleaning data..."
  for autompg_datum_raw in autompg_data_raw:
      splitArr = autompg_datum_raw.split(',')
      tempList = list()
      for j in range(0, len(splitArr)):
	  tempList.append(str.strip(splitArr[j]))
      autompg_data.append(tempList)

  print "normalizing data..."
  normalize(autompg_data)
  print "...normalized data"

  print "discretizing the data..."
  discretize(autompg_data)
  Dataholder = dataHolder(autompg_data)
  print "finished cleaning data\nBuilding tree..."
  node = buildtree(None, Dataholder, None, Dataholder)

  print "built tree\nreading test data..."
  #print_node(node)
  # main program ends
  #######################################################################################################################
  # validation begins

  datast = list()

  f = open(testDataSetName, 'r')
  autompg_test_raw = f.readlines()
  f.close()
  # end read from autompg datafile user lists
  autompg_test = list()
  print "finished reading test data\ncleaning test..."
  for autompg_t_item_raw in autompg_test_raw:
      splitTArr = autompg_t_item_raw.split(',')
      tempTList = list()
      for j in range(0, len(splitTArr)):
	  tempTList.append(str.strip(splitTArr[j]))
      autompg_test.append(tempTList)


  print "normalizing test..."
  normalize(autompg_test)
  print "...normalized test\ndiscretizing test..."

  discretize(autompg_test)
  print "...discretized test\nfinished reading test\nstarting classification..."
  testingNodesList = dict()
  classifiedNodesList = dict()
  i = 0
  
  outputFilename = ""
  if option == 1:
    outputFilename = "output_decisiontree_pca.txt"
  elif option == 2:
    outputFilename = "output_decisiontree_correlation.txt"
  elif option == 3:
    outputFilename = "output_decisiontree_variance.txt"
  else:
    outputFilename = "output_decisiontree_nored.txt"
    
  f_out = open(outputFilename, 'w')
  
  for datarow in autompg_test:
      testingNodesList[i] = datarow[len(datarow)-1]
      classifiedNode = classify(datarow, node)
      #print datarow,
      #f_out.write(testingNodesList[i])
      if isinstance(classifiedNode, SimpleNode):
	  #print classifiedNode.name
	  classifiedNodesList[i] = classifiedNode.name
      else:
	  #print classifiedNode
	  classifiedNodesList[i] = classifiedNode
      f_out.write(classifiedNodesList[i])
      i += 1
  print "\nfinished classifying\ncalculating accuracy..."

  f_out.close()

  predicted_write(classifiedNodesList,option)

  predictedCorrectValues = 0
  for i in range(0, len(testingNodesList)):
      if testingNodesList[i] == classifiedNodesList[i]:
	  predictedCorrectValues += 1



  accuracy = (float(predictedCorrectValues)/len(testingNodesList)) * 100
  print "Found Accuracy:", accuracy, "%"

  # validation ends
#######################################################################################################################
