from sklearn import tree, svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import numpy as np
import numpy.matlib
import math

def readData(filename, trainPercent = 0.3):
    f = open(filename, 'r')
    data = np.loadtxt(f, delimiter = ';')
    np.random.shuffle(data)
    trainN = int(math.floor( trainPercent * data.shape[0] ))    
    testN = data.shape[0] - trainN
    train = data[0:trainN-1, :]
    test  = data[trainN:data.shape[0], :]
    return train, test
    
def testPrecision(classifier, data):
    trueRate = 0.0
    falseRate = 0.0
    for test in data:
        predClass = classifier.predict(test[0])
        realClass = test[1]
        #print str(predClass) + " " + str(realClass)
        if predClass == realClass:
            trueRate += 1
        else:
            falseRate += 1
    
    trueRate /= len(data)
    falseRate /= len(data)
    
    print "True  rate: " + str(trueRate) + "%"
    print "False rate: " + str(falseRate) + "%"

if __name__ == '__main__':
    
    class1train, class1test = readData("1_Adeykin.csv")
    class3train, class3test = readData("3_Adeykin.csv")
    class4train, class4test = readData("4_Adeykin.csv")
    class10train, class10test = readData("10_Adeykin.csv")
    class13train, class13test = readData("13_Adeykin.csv")
    class14train, class14test = readData("14_Adeykin.csv")
    class15train, class15test = readData("15_Adeykin.csv")
    class16train, class16test = readData("16_Adeykin.csv")
    
    train = np.concatenate( (class1train, class3train, class4train, class10train, class13train, class14train, class15train, class16train) )

    print "SIZE = " + str(class1train.shape[0])
    """
    y1 = np.matlib.full( (class1train.shape[0], 1), 1 )
    y3 = np.matlib.full( (class3train.shape[0], 1), 3 )
    y4 = np.matlib.full( (class4train.shape[0], 1), 4 )
    y10 = np.matlib.full( (class10train.shape[0], 1), 10 )
    y13 = np.matlib.full( (class13train.shape[0], 1), 13 )
    y14 = np.matlib.full( (class14train.shape[0], 1), 14 )
    y15 = np.matlib.full( (class15train.shape[0], 1), 15 )
    y16 = np.matlib.full( (class16train.shape[0], 1), 16 )
    
    y = np.concatenate( (y1, y3, y4, y10, y13, y14, y15, y16) )
    """
    y = [1]*class1train.shape[0] + [3]*class3train.shape[0] + [4]*class4train.shape[0] + [10]*class10train.shape[0] + [13]*class13train.shape[0] + [14]*class14train.shape[0] + [15]*class15train.shape[0] + [16]*class16train.shape[0]
    
    
      
    testCouplesList = [(class1test[i, :], 1) for i in range(class1test.shape[0])] + \
                      [(class3test[i, :], 3) for i in range(class3test.shape[0])] + \
                      [(class4test[i, :], 4) for i in range(class4test.shape[0])] + \
                      [(class10test[i, :], 10) for i in range(class10test.shape[0])] + \
                      [(class13test[i, :], 13) for i in range(class13test.shape[0])] + \
                      [(class14test[i, :], 14) for i in range(class14test.shape[0])] + \
                      [(class15test[i, :], 15) for i in range(class15test.shape[0])] + \
                      [(class16test[i, :], 16) for i in range(class16test.shape[0])]
    
    for i in range(1,4):            
        classifier = KNeighborsClassifier(n_neighbors=i)
        classifier = classifier.fit(train, y)    
        print "KNN learning succesfull finished " + str(i)
        testPrecision(classifier, testCouplesList)
    
    classifier = tree.DecisionTreeClassifier()
    classifier = classifier.fit(train, y)
    print "Decision tree learning succesfull finished "
    testPrecision(classifier, testCouplesList)
    
    classifier = GaussianNB()
    classifier = classifier.fit(train, y)
    print "Naive Bayes learning succesfull finished "
    testPrecision(classifier, testCouplesList)
    
    classifier = svm.SVC()
    classifier = classifier.fit(train, y)
    print "SVC learning succesfull finished "
    testPrecision(classifier, testCouplesList)
    """
    classifier = svm.SVC(decision_function_shape='ovo')
    classifier = classifier.fit(train, y)
    print "SVC OVO learning succesfull finished "
    testPrecision(classifier, testCouplesList)
    """
    classifier = svm.NuSVC()
    classifier = classifier.fit(train, y)
    print "NuSVC learning succesfull finished "
    testPrecision(classifier, testCouplesList)
    
    classifier = svm.LinearSVC()
    classifier = classifier.fit(train, y)
    print "LinearSVC learning succesfull finished "
    testPrecision(classifier, testCouplesList)

    
    
