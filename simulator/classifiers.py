import utils

class Classifiers(object):

    def __init__(self, row = 10, column = 10):
        # Threshold for classifier prediction
        self.THRESHOLD = .5
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
        self.classifierNames = ('corner', 'doorway', 'garbagecan', 'table', 'litterbox', 'closet')
        self.classifiers['corner'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['doorway'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['garbagecan'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['table'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['litterbox'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['closet'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers = dict()
        self.normalizedClassifiers['corner'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['doorway'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['garbagecan'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['table'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['litterbox'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['closet'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
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
                if sample[i][j] >= 1:
                    self.classifiers[label][i][j]['dirt given C'] += 1
                    self.update_other_classifiers(label, 'dirt given not C', (i, j))
                elif sample[i][j] == 0:
                    self.classifiers[label][i][j]['none given C'] += 1
                    self.update_other_classifiers(label, 'none given not C', (i, j))
                elif sample[i][j] == -1:
                    self.classifiers[label][i][j]['obs given C'] += 1
                    self.update_other_classifiers(label, 'obs given not C', (i, j))
        for label in self.classifierNames:
            self.normalize(label)

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

    def getClassifier(self, classifier):
        return self.normalizedClassifiers[classifier]

    def chooseBestClassifier(self, inputGrid):
        # Gets yes probabilites
        probs = [(classifier, self.getLikelyhood(classifier, inputGrid)[0]) for classifier in self.classifierNames]

        # Calculates new probabilities
        from operator import itemgetter
        maxClassifier = max(probs, key = itemgetter(1))

        if maxClassifier[1] >= self.THRESHOLD:
            return maxClassifier[0]
        else:
            return "None"


    def getLikelyhood(self, classifier, inputGrid):
        probYes, probNo = 1 , 1
        for i in range(self.sampleRowSize):
            for j in range(self.sampleColumnSize):
                if inputGrid[i][j] >= 1:
                    probYes *= self.normalizedClassifiers[classifier][i][j]['dirt given C']
                    probNo *= self.normalizedClassifiers[classifier][i][j]['dirt given not C']
                elif inputGrid[i][j] == 0:
                    probYes *= self.normalizedClassifiers[classifier][i][j]['none given C']
                    probNo *= self.normalizedClassifiers[classifier][i][j]['none given not C']
                elif inputGrid[i][j] == -1:
                    probYes *= self.normalizedClassifiers[classifier][i][j]['obs given C']
                    probNo *= self.normalizedClassifiers[classifier][i][j]['obs given not C']

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

        return (probYes, probNo)


    def laplaceSmoothing(self, num = 4):
        for name in self.classifierNames:
            for i in range(self.sampleRowSize):
                for j in range(self.sampleColumnSize):
                    self.classifiers[name][i][j]['dirt'] += num
                    self.classifiers[name][i][j]['none'] += num
                    self.classifiers[name][i][j]['obs'] += num
        self.normalize()

    def featureExtraction(self, inmap):
        assert(inmap.isinstance(map.Environment))

        #to start with, just uses every blocksize x blocksize section
        blockSize = 10
        xRange = int(inmap.widthCells - blockSize - 1)
        yRange = int(inmap.heightCells - blockSize - 1)
        for y in xrange(0, yRange):
            for x in xrange(0, xRange):
                #Run classifier on block
                #Limits of this block are [x, x+blockSize] and [y, y+blockSize]
                continue


# Test Cases
'''
x = Classifiers()
sample = [[1,2,3,0,-1],[0,0,0,0,0]]
x.train(sample, 'chair')
sample2 = [[0,1,3,2,1],[0,0,0,0,0]]
x.train(sample2, 'chair')
'''

y = Classifiers(10, 10)


from os import listdir
mypath = '../assets/training_maps'
onlyfiles = [f for f in listdir(mypath)]

for file in onlyfiles:
    pathToMap = './../assets/training_maps/' + file
    classifier = file.split('_')[0]
    map = utils.readTrainingMap(pathToMap)
    y.train(map, classifier)
x = 0