import utils

class Classifiers(object):

    def __init__(self, row = 2, column = 5):
        self.classifiers = dict()
        self.sampleRowSize = row
        self.sampleColumnSize = column
        cellValue = dict()
        cellValue['none'] = 0.0
        cellValue['dirt'] = 0.0
        cellValue['obs'] = 0.0
        self.classifierNames = ('openCell', 'doorway', 'garbageCan', 'chair', 'litterBox', 'houseEntrance')
        self.classifiers['openCell'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['doorway'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['garbageCan'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['chair'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['litterBox'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.classifiers['houseEntrance'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers = dict()
        self.normalizedClassifiers['openCell'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['doorway'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['garbageCan'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['chair'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['litterBox'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
        self.normalizedClassifiers['houseEntrance'] = [[cellValue.copy() for x in range(self.sampleColumnSize)]
                                        for y in range(self.sampleRowSize)]
    '''
    In train you are given a list of lists matrix for the sample
    This sample then has either noen, obs, and dirt for each  cell.
    Based on this then probabilities are then updated for each cell, as we go through.
    '''
    def train(self, sample, label):
        for i in range(self.sampleRowSize):
            for j in range(self.sampleColumnSize):
                y = sample[i][j]
                if sample[i][j] >= 1:
                    self.classifiers[label][i][j]['dirt'] += 1
                elif sample[i][j] == 0:
                    self.classifiers[label][i][j]['none'] += 1
                elif sample[i][j] == -1:
                    self.classifiers[label][i][j]['obs'] += 1
        self.normalize(label)

    '''
    Helper function:
    Only task is to normalize after adding values
    '''
    def normalize(self, classifier):
        for i in range(self.sampleRowSize):
            for j in range(self.sampleColumnSize):
                pred = self.classifiers[classifier][i][j].copy()
                total = sum(pred.values())
                for key in pred.keys():
                    pred[key] = pred[key] / total
                self.normalizedClassifiers[classifier][i][j] = pred

    def getClassifier(self, classifier):
        return self.classifiers[classifier]

    def laplaceSmoothing(self, num = 4):
        for name in self.classifierNames:
            for i in range(self.sampleRowSize):
                for j in range(self.sampleColumnSize):
                    self.classifiers[name][i][j]['dirt'] += num
                    self.classifiers[name][i][j]['none'] += num
                    self.classifiers[name][i][j]['obs'] += num
        self.normalize()




# Test Cases

x = Classifiers()
sample = [[1,2,3,0,-1],[0,0,0,0,0]]
x.train(sample, 'chair')
sample2 = [[0,1,3,2,1],[0,0,0,0,0]]
x.train(sample2, 'chair')

y = Classifiers(10, 10)
mapTest = utils.readTrainingMap('./../assets/training_maps/chair_0.csv')
y.train(mapTest, 'chair')
y.laplaceSmoothing()