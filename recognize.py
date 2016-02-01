from sklearn.neighbors import KNeighborsClassifier
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

    y1 = np.matlib.full( (class1train.shape[0], 1), 1 )
    y3 = np.matlib.full( (class3train.shape[0], 1), 3 )
    y4 = np.matlib.full( (class4train.shape[0], 1), 4 )
    y10 = np.matlib.full( (class10train.shape[0], 1), 10 )
    y13 = np.matlib.full( (class13train.shape[0], 1), 13 )
    y14 = np.matlib.full( (class14train.shape[0], 1), 14 )
    y15 = np.matlib.full( (class15train.shape[0], 1), 15 )
    y16 = np.matlib.full( (class16train.shape[0], 1), 16 )
    
    y = np.concatenate( (y1, y3, y4, y10, y13, y14, y15, y16) )

    classifier = KNeighborsClassifier(n_neighbors=3)
    classifier.fit(train, y)
    
    