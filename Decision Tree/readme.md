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