import utils

class Classifiers(object):

    def __init__(self, row = 10, column = 10):
        # Threshold for classifier prediction
        self.THRESHOLD = 0.90            # .792 is good for test, .88 is good  for goodhouse
        self.classifiers = dict()
        self.sampleRowSize = row
        self.sampleColumnSize = column
        cellValue = dict()
        cellValue['none given C'] = 0.0
        cellValue['dirt given C'] = 0.0
        cellValue['obs given C'] = 0.0
        cellValue['none given not C'] = 0.0
        cellValue['dirt given not C'] = 0.0
        cellValue['obs given not C'] = 0.0
        self.classifierNames = self.importClassifers()
        self.normalizedClassifiers = dict()

        for name in self.classifierNames:
            self.classifiers[str(name)] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]

            self.normalizedClassifiers[str(name)] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.train_with_files()
        self.laplaceSmoothing(55)

    def importClassifers(self):
        from os import listdir
        mypath = '../assets/training_maps'
        onlyfiles = [f for f in listdir(mypath)]
        classifiers = list()

        for file in onlyfiles:
            classifier = file.split('_')[0]
            if classifier not in classifiers:
                classifiers.append(classifier)
        return classifiers

    def train_with_files(self):
        from os import listdir
        mypath = '../assets/training_maps'
        onlyfiles = [f for f in listdir(mypath)]

        for file in onlyfiles:
            pathToMap = './../assets/training_maps/' + file
            classifier = file.split('_')[0]
            map = utils.readTrainingMap(pathToMap)
            self.train(map, classifier)


    '''
    In train you are given a list of lists matrix for the sample
    This sample then has either noen, obs, and dirt for each  cell.
    Based on this then probabilities are then updated for each cell, as we go through.
    '''
    def train(self, sample, label):
        if label not in self.classifierNames:
            raise Exception("Invalid classifier name " + label)
        for i in range(self.sampleRowSize):
            for j in range(self.sampleColumnSize):
                y = sample[i][j]
                if 1 <= sample[i][j] <= 3:
                    self.classifiers[label][i][j]['dirt given C'] += 1
                    self.update_other_classifiers(label, 'dirt given not C', (i, j))
                elif sample[i][j] == 0:
                    self.classifiers[label][i][j]['none given C'] += 1
                    self.update_other_classifiers(label, 'none given not C', (i, j))
                elif sample[i][j] == -1:
                    self.classifiers[label][i][j]['obs given C'] += 1
                    self.update_other_classifiers(label, 'obs given not C', (i, j))
                else:
                    raise Exception("Invalid training map, bad cell value")
        for label in self.classifierNames:
            self.normalize(label)

    '''
    Helper Function:
    Task is to update every other classifier with evidence
    '''
    def update_other_classifiers(self, label, evidence, coord):
        namesToUpdate = [name for name in self.classifierNames if name != label ]
        for name in namesToUpdate:
            self.classifiers[name][coord[0]][coord[1]][evidence] += 1



    '''
    Helper function:
    Only task is to normalize after adding values
    '''
    def normalize(self, classifier):
        for i in range(self.sampleRowSize):
            for j in range(self.sampleColumnSize):
                pred = self.classifiers[classifier][i][j].copy()
                sumC , sumNotC = 0 , 0
                for key in pred.keys():
                    if "not C" in key:
                        sumNotC += pred[key]
                    else:
                        sumC += pred[key]
                for key in pred.keys():
                    if "not C" in key:
                        if sumNotC != 0:
                            pred[key] = pred[key] / sumNotC
                        else:
                            pred[key] = 0
                    else:
                        if sumC != 0:
                            pred[key] = pred[key] / sumC
                        else:
                            pred[key] = 0
                self.normalizedClassifiers[classifier][i][j] = pred
    '''
    Test function should not be really used
    '''
    def getClassifier(self, classifier):
        return self.normalizedClassifiers[classifier]

    '''
    Goes trhough and gets likelyhood for each classifier
    then chooses threshold with max likelyhood
    if likelyhood is greater than threshold then returns that otherwise returns none
    '''
    def getBestClassifier(self, inputGrid):
        all_possible_grids = utils.generateMapOrientations(inputGrid)
        probs = list()

        for classifier in self.classifierNames:
            values = [self.getLikelyhood(classifier, inputGrid)[0] for inputGrid in all_possible_grids]
            maxValue = max(values)
            probs.append((classifier, maxValue))

        # Gets yes probabilites
        probs = [(classifier, self.getLikelyhood(classifier, inputGrid)[0]) for classifier in self.classifierNames]
        #print probs
        # Calculates new probabilities
        from operator import itemgetter
        maxClassifier = max(probs, key=itemgetter(1))

        if maxClassifier[1] >= self.THRESHOLD:
            return maxClassifier[0]
        else:
            return None


    def getLikelyhood(self, classifier, inputGrid):
        probYes, probNo = 1 , 1
        for i in range(self.sampleRowSize):
            for j in range(self.sampleColumnSize):
                if 1 <= inputGrid[i][j] <= 3:
                    probYes *= self.normalizedClassifiers[classifier][i][j]['dirt given C']
                    probNo *= self.normalizedClassifiers[classifier][i][j]['dirt given not C']
                elif inputGrid[i][j] == 0:
                    probYes *= self.normalizedClassifiers[classifier][i][j]['none given C']
                    probNo *= self.normalizedClassifiers[classifier][i][j]['none given not C']
                elif inputGrid[i][j] == -1:
                    probYes *= self.normalizedClassifiers[classifier][i][j]['obs given C']
                    probNo *= self.normalizedClassifiers[classifier][i][j]['obs given not C']
                elif inputGrid[i][j] == None:
                    continue
                else:
                    raise Exception("Invalid input grid given to get classifier")

        pred = self.classifiers[classifier][0][0].copy()
        sumC , sumNotC = 0 , 0
        for key in pred.keys():
            if "not C" in key:
                sumNotC += pred[key]
            else:
                 sumC += pred[key]
        tot = sumC + sumNotC
        sumC /= tot
        sumNotC /= tot

        probYes *= sumC
        probNo *= sumNotC

        tot = probNo + probYes
        probNo /= tot
        probYes /= tot

        return (probYes, probNo)


    def laplaceSmoothing(self, num = 4):
        for classifier in self.classifierNames:
            for i in range(self.sampleRowSize):
                for j in range(self.sampleColumnSize):
                    self.classifiers[classifier][i][j]['dirt given C'] += num
                    self.classifiers[classifier][i][j]['dirt given not C'] += num
                    self.classifiers[classifier][i][j]['none given C'] += num
                    self.classifiers[classifier][i][j]['none given not C'] += num
                    self.classifiers[classifier][i][j]['obs given C'] += num
                    self.classifiers[classifier][i][j]['obs given not C'] += num
            self.normalize(classifier)




# Test Cases
'''
x = Classifiers()
sample = [[1,2,3,0,-1],[0,0,0,0,0]]
x.train(sample, 'chair')
sample2 = [[0,1,3,2,1],[0,0,0,0,0]]
x.train(sample2, 'chair')
'''

'''

y = Classifiers()

testMap = '../assets/training_maps/doorway_1.csv'
testMap = '../assets/maps/obstacle.csv'
testMap = utils.readTrainingMap(testMap)
z = y.getBestClassifier(testMap)
x = 0


sample2 = [[0, 1, 3, 2, 1],
           [0, 0, 0, 0, 0],
           [1, 1, 3, 0, 1],
           [0, 1, 0, 0, 0]]

submatrix = sample2[0:3]
submatrix = submatrix[:][0:2]

submatrix = [[sample2[i][j] for i in range(2)] for j in range(2)]



x = 0
'''
