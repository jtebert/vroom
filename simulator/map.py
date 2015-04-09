
import time
import pygame
from pygame. locals import *
from math import ceil, floor, atan2, degrees, radians, sqrt
import csv

MAX_DIRT = 3

#Probalistic Distributions per dirt level based on obstacle label
# "dirtValue" : [ p(accum. dirt) , p(spreading) ]
openCellDist = { "0" : [.1,0] , "1" : [.20,.01] , "2" : [.20, .05] , "3" : [.0,.2] }
doorwayDist =  { "0" : [.8,0] , "1" : [.20,0] , "2" : [.20, .05] , "3" : [.0,.2] }
garbageCanDist = { "0" : [.8,0] , "1" : [.20,0] , "2" : [.20, .05] , "3" : [.0,.2] }
chairDist = { "0" : [.8,0] , "1" : [.20,0] , "2" : [.20, .05] , "3" : [.0,.2] }
litterBoxDist = { "0" : [.8,0] , "1" : [.20,0] , "2" : [.20, .05] , "3" : [.0,.2] }
houseEntranceDist = { "0" : [.8,0] , "1" : [.20,0] , "2" : [.20, .05] , "3" : [.0,.2] }

labelDict = { "openCell": openCellDist, 
              "doorway": doorwayDist, 
              "garbageCan": garbageCanDist, 
              "chair": chairDist, 
              "litterBox": litterBoxDist, 
              "houseEntrance" : houseEntranceDist }

class MapNode(object):
    
    def __init__(self):
        self.isObstacle = False
        self.isVisited = False
        self.dirt = 0
        self.label = None
        self.value = 0


class RobotMap(object):
    center = (0,0)

    def __init__(self,w=700,h=700,cellXSize=10,cellYSize=10):
        self.scale = 1.0
        self.cellXSize = cellXSize
        self.cellYSize = cellYSize
        self.width = w
        self.height = h
        self.boundingBox = ((w/2,h/2),(w/2,h/2))
        self.xCells = w/cellXSize
        self.yCells = h/cellYSize
        self.dirtCells = []
        self.visitedCells = []
        self.obstacles = []

        #TODO to get unvisited cells to work right we need the map cells
        #depend on the input environment
        self.unvisitedCells = []

        self.map = [[MapNode() for columns in xrange(self.width/cellXSize)] for rows in xrange(self.height/cellYSize)]

    def draw(self,screen, environment = None):

        s = screen.get_size()
        sx = self.scale*float(s[0])/self.width
        sy = self.scale*float(s[1])/self.height
        center = (0,0)


        halfWidthMap = ceil(self.width/(2.*self.scale))
        halfHeightMap = ceil(self.height/(2.*self.scale))

        minx,miny,maxx,maxy =  (max(center[0]-halfWidthMap,0),
                                max(center[1]-halfHeightMap,0),
                                min(center[0]+halfWidthMap,self.width),
                                min(center[1]+halfHeightMap,self.height))

        cellXMax = self.width/self.cellXSize
        cellYMax = self.height/self.cellYSize

        for x in xrange(0,int(cellXMax)):
            for y in xrange(0,int(cellYMax)):
                cellCornerX = x*self.cellXSize
                cellCornerY = y*self.cellYSize
                r = pygame.Rect(cellCornerX, cellCornerY, self.cellXSize, self.cellYSize)

                if environment != None:
                    if environment.map[x][y].value == -1:
                        pygame.draw.rect(screen,(0,0,0),r,0)
                    elif environment.map[x][y].value == 0:
                        pygame.draw.rect(screen,(255,255,255),r,0)
                    elif environment.map[x][y].dirt > 0:
                        d = environment.map[x][y].dirt
                        pygame.draw.rect(screen,(0,0,255-(40*d)),r,0)

                else:
                    if self.map[x][y].isObstacle:
                        pygame.draw.rect(screen,(0,0,0),r,0)
                    elif (self.map[x][y].dirt > 0):
                        d = self.map[x][y].dirt
                        pygame.draw.rect(screen,(0,0,255-(40*d)),r,0)
                    elif self.map[x][y].isVisited:
                        pygame.draw.rect(screen,(255,255,255),r,0)


    def drawRobot (self,screen,robot):


        for x in range(-2,3,1):
            for y in range (-2,3,1):
                self.map[robot.pos[0]+x][robot.pos[1]+y].isVisited = True

                if ((robot.pos[0]+x,robot.pos[1]+y) not in self.visitedCells):
                    self.visitedCells.append((robot.pos[0]+x,robot.pos[1]+y))



        minx,miny,maxx,maxy =  (max((robot.pos[0]*self.cellXSize)-(robot.size)/2,0),
                                max((robot.pos[1]*self.cellYSize)-(robot.size)/2,0),
                                min((robot.pos[0]*self.cellXSize)+(robot.size)/2,self.width),
                                min((robot.pos[1]*self.cellYSize)+(robot.size)/2,self.height))
        
        
        robotLeftCornerX = ((robot.pos[0]-2)*self.cellXSize)
        robotLeftCornerY = ((robot.pos[1]-2)*self.cellXSize)
        robotCenterX = (robot.pos[0]*self.cellXSize)+(self.cellXSize/2)
        robotCenterY = (robot.pos[1]*self.cellXSize)+(self.cellYSize/2)

        r = pygame.Rect(robotLeftCornerX,robotLeftCornerY, robot.size, robot.size)
        pygame.draw.rect(screen,(0,0,0),r, 1)

        if robot.heading == 'North':
            pygame.draw.line(screen,(255,0,0),(robotCenterX,robotCenterY),(robotCenterX,robotCenterY-robot.size))
        if robot.heading == 'South':
            pygame.draw.line(screen,(255,0,0),(robotCenterX,robotCenterY),(robotCenterX,robotCenterY+robot.size))
        
        if robot.heading == 'East':
            pygame.draw.line(screen,(255,0,0),(robotCenterX,robotCenterY),(robotCenterX+robot.size,robotCenterY))

        if robot.heading == 'West':
            pygame.draw.line(screen,(255,0,0),(robotCenterX,robotCenterY),(robotCenterX-robot.size,robotCenterY))



    def copy (self):
        mapcp = RobotMap()
        mapcp.dirtCells = list(self.dirtCells)
        mapcp.visitedCells = list(self.visitedCells)
        mapcp.obstacles = list(self.obstacles)
        mapcp.unvisitedCells = list(self.unvisitedCells)

        cellXMax = self.width/self.cellXSize
        cellYMax = self.height/self.cellYSize

        for x in xrange(0,int(cellXMax)):
            for y in xrange(0,int(cellYMax)):
                mapcp.map[x][y] = self.map[x][y]
        
        
        return mapcp

class Environment(object):
    center = (0,0)


    def __init__(self,environmentCSV = './../assets/maps/test.csv',w=700,h=700,cellXSize=10,cellYSize=10):
        self.cellXSize = cellXSize
        self.cellYSize = cellYSize
        self.width = w
        self.widthCells = w / cellXSize
        self.height = h
        self.heightCells = h / cellYSize
        self.boundingBox = ((w/2,h/2),(w/2,h/2))
        self.label = ''
        self.map = [[MapNode() for columns in xrange(self.width/cellXSize)] for rows in xrange(self.height/cellYSize)]


        self.importEnviroment(environmentCSV)

    def copy (self):
        mapcp = Environment()

        cellXMax = self.width/self.cellXSize
        cellYMax = self.height/self.cellYSize

        for x in xrange(0,int(cellXMax)):
            for y in xrange(0,int(cellYMax)):
                mapcp.map[x][y] = self.map[x][y]

        return mapcp

    def adjacent(self, x, y):
        # Returns the adjacent cells to one cell (the other ones that will impact the amount of dirt in a given cell)
        try:
            adjCells = [(self.map[x + 1][y]), (self.map[x - 1][y]), (self.map[x][y + 1]), (self.map[x][y - 1])]
        except:
            print x
            print y
            raise

        return adjCells

    def addDirt(self,currentDirt, newDirt):
        # Returns amount of dirt after adding newDirt to currentDirt
        return min(MAX_DIRT, currentDirt + newDirt)

    def updateDirt(self):
        # Updates dirt by adding more based on however much is there to begin with and the adjacent cells
        #Todo: seeding
        import random

        mapCopy = self.copy() #Check copy so dirt doesn't cascade across the map from earlier checks


        for y in xrange(0,int(mapCopy.heightCells-1)):
            for x in xrange(0,int(mapCopy.widthCells-1)):

                if mapCopy.map[x][y].isObstacle:
                    #Obstacle that can't be cleaned
                    continue

                elif mapCopy.map[x][y].value == None:
                    #its a cell not in the environment
                    continue

                elif mapCopy.map[x][y].label == None:
                    randomVal = random.random()
                    cellDist = openCellDist[str(mapCopy.map[x][y].dirt)]
                    
                    #Own cell: default dirt generation
                    if random.random() < cellDist[0]:
                        print "dirt before : ",self.map[x][y].dirt
                        self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)
                        print "dirt after : ",self.map[x][y].dirt

                

                else:
                    #Own cell: Generation based on label
                    if random.random() >= labelDict[str(mapCopy.map[x][y].label)][str(mapCopy.map[x][y].dirt)]:
                        self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)

                #Dirt generation from adjacent cells
                for cell in mapCopy.adjacent(x, y):
                    if cell.isObstacle:
                        continue

                    elif cell.value == None:
                        continue

                    elif cell.label == None:
                        randomVal = random.random()
                        cellDist = openCellDist[str(mapCopy.map[x][y].dirt)]
                       
                    
                        #Adjacent cell: default dirt generation
                        if randomVal < cellDist[1]:
                            dirtAdd = self.addDirt(self.map[x][y].dirt, 1)
                            self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)

                    else:
                        #Adjacent cell: Generation based on label
                        if random.random() >= labelDict[str(mapCopy.map[x][y].label)][str(mapCopy.map[x][y].dirt)]:
                            self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)

    def importEnviroment(self,csvFile):

        with open(csvFile,'r') as csvFile:
            i = 0
            j = 0
            reader = csv.reader(csvFile)
            for row in reader:
                for column in row:
                    if j > (self.width/self.cellXSize):
                        break
                    if(column != ''):
                        if '[' in column:
                            column = column.replace('[','')
                            column = column.split(',')

                            value = int(column[0])
                            if value > 0:
                                self.map[i][j].dirt = value
                            else:
                                self.map[i][j].isObstacle = True

                            self.map[i][j].value = int(column[0])
                            self.map[i][j].label = column[1]
                        else:
                            
                            value = int(column)
                            if value > 0:
                                self.map[i][j].dirt = value
                            else:
                                self.map[i][j].isObstacle = True

                            self.map[i][j].value = int(column)
                    else:
                        self.map[i][j].value = None
                    i += 1
                i = 0
                j += 1

                if j > (self.height/self.cellYSize):
                    break
            return
                
    
    

 



 
