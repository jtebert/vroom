
import time
import pygame
from pygame. locals import *
from math import ceil, floor, atan2, degrees, radians, sqrt
import csv

MAX_DIRT = 3

#Probalistic Distributions per dirt level based on obstacle label
# "dirtValue" : [ p(accum. dirt) , p(spreading) ]
openCellDist = { "0" : [.000,0] , "1" : [.00,.01] , "2" : [.10, .05] , "3" : [.0,.1] }
doorwayDist =  { "0" : [.4,0] , "1" : [.1,0] , "2" : [.1, .05] , "3" : [.0,.2] }
garbageCanDist = { "0" : [.4,0] , "1" : [.1,0] , "2" : [.1, .05] , "3" : [.0,.2] }
tableDist = { "0" : [.4,0] , "1" : [.1,0] , "2" : [.1, .05] , "3" : [.0,.2] }
litterBoxDist = { "0" : [.4,0] , "1" : [.1,0] , "2" : [.1, .05] , "3" : [.0,.2] }
closetDist = { "0" : [.4,0] , "1" : [.1,0] , "2" : [.1, .05] , "3" : [.0,.2] }
cornerDist = { "0" : [.4,0] , "1" : [.1,0] , "2" : [.1, .05] , "3" : [.0,.2] }

labelDict = { "openCell": openCellDist, 
              "doorway": doorwayDist, 
              "garbageCan": garbageCanDist, 
              "garbagecan": garbageCanDist,
              "table": tableDist,
              "litterBox": litterBoxDist, 
              "litterbox": litterBoxDist, 
              "closet" : closetDist,
              "corner" : cornerDist,
              "None" : openCellDist }

class MapNode(object):
    
    def __init__(self, row, col):
        self.isObstacle = False
        self.isVisited = False
        self.dirt = 0
        self.label = None
        self.value = None
        self.validActions = []
        self.row = row
        self.col = col

    def __str__(self):
        if self.isVisited:
            return "1"
        else:
            return "0"

    def set_valid_actions(self, robot_state):
        """
        Use the robot state to determine explorative actions from the current cell
        """
        new_actions = []
        actions = robot_state.getLegalActions((self.col, self.row))
        for a in actions:
            if robot_state.willVisitNewCell((self.col, self.row), a):
                new_actions.append(a)
        self.validActions = new_actions

    def are_any_valid_actions(self):
        return len(self.validActions) > 0


    def copy(self, row, col):
        nodeCp = MapNode(row,col)
        nodeCp.isObstacle = bool(self.isObstacle)
        nodeCp.isVisited = bool(self.isVisited)
        nodeCp.dirt = int(self.dirt)

        if self.label != None:
            nodeCp.label = str(self.label)
        else:
            nodeCp.label = None
            
        if self.value != None:
            nodeCp.value = int(self.value)
        else:
            nodeCp.value = None

        nodeCp.validActions = list(self.validActions)
        nodeCp.row = row
        nodeCp.col = col
        return nodeCp

class RobotMap(object):
    center = (0,0)

    def __init__(self,w=700,h=700,cellXSize=10,cellYSize=10,map=True):
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
        self.robotPositions = []

        self.unvisitedCells = []
        self.observedCells = []  #cells seen by the proximity sensor, but not visited
        
        if(map):
            self.map = [[MapNode(rows, columns) for columns in xrange(self.width/cellXSize)] for rows in xrange(self.height/cellYSize)]
            for x in xrange(0,int(self.xCells)):
                for y in xrange(0,int(self.yCells)):
                    self.unvisitedCells.append([x,y])
        else:
            self.map = None
              



    def __str__(self):
        print_str = ""
        for row in range(self.yCells):
            for col in xrange(self.xCells):
                print_str += (str(self.map[row][col]) + " ")
            print_str += "\n"
        return print_str
        

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
                        pygame.draw.rect(screen,(0,0,255-(60*d)),r,0)

                else:
                    if self.map[x][y].isObstacle:
                        pygame.draw.rect(screen,(0,0,0),r,0)
                    elif (self.map[x][y].dirt > 0):
                        d = self.map[x][y].dirt

                        pygame.draw.rect(screen,(0,0,255-(60*d)),r,0)
                    elif self.map[x][y].isVisited:
                        pygame.draw.rect(screen,(255,255,255),r,0)


    def drawRobot (self,screen,robot):



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


    def drawLabels(self, screen):
        """
        For each group of map labels, draw the label in text
        """
        
        isDrawn = []
        
        for row in range(self.yCells):
            for col in range(self.xCells):
                #assumes it hits the top left corner of a group of labels
                #and that the labels are 10x10
                if self.map[col][row].label != None: 
                    if [col,row] not in isDrawn:
                        myfont = pygame.font.SysFont("Comic Sans MS", 16)
                        # apply it to text on a label
                        #print self.map[col][row].label
                        label = myfont.render(str(self.map[col][row].label), 1, (0,0,0))
                        labelPos = ((col+2)*self.cellYSize, (row+3)*self.cellXSize)
                        screen.blit(label, labelPos)

                        r = pygame.Rect((col)*self.cellYSize,(row)*self.cellXSize, 100, 100)
                        pygame.draw.rect(screen,(255,0,0),r, 2)
                        

                        for i in range(10):
                            for j in range(10):
                                isDrawn.append([col+i,row+j])
                    
        return True


    def are_all_visited(self):
        """
        Check if all explorable cells have been explored.
        If all visited, search mapping is complete
        :return: Boolean, fully explored or not
        """
        for row in range(self.yCells):
            for col in range(self.xCells):
                if self.map[col][row].are_any_valid_actions():
                    return False
        return True

    def set_all_valid_actions(self, robot_state):
        """
        Use the robot state to determine what actions are valid,
        ONLY for cells that have been visited.
        :param robot_state: RobotState (for the map)
        :return: Nothing. Mutation, man.
        """
        for row in range(self.yCells):
            for col in range(self.xCells):
                if self.map[col][row].isVisited:
                    self.map[col][row].set_valid_actions(robot_state)

    def copy (self, copyMap=False):
        mapcp = RobotMap(map=copyMap)
        mapcp.dirtCells = list(self.dirtCells)
        mapcp.visitedCells = list(self.visitedCells)
        mapcp.obstacles = list(self.obstacles)
        mapcp.unvisitedCells = list(self.unvisitedCells)
        mapcp.observedCells = list(self.observedCells)
        mapcp.robotPositions = list(self.robotPositions)

        cellXMax = self.width/self.cellXSize
        cellYMax = self.height/self.cellYSize

        if copyMap:
            for x in xrange(0,int(mapcp.xCells)):
                for y in xrange(0,int(mapcp.yCells)):
                    mapcp.map[x][y] = self.map[x][y].copy(y,x)

        else:
            mapcp.map = self.map
        
        
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

    def addDirt(self, currentDirt, newDirt):
        # Returns amount of dirt after adding newDirt to currentDirt
        return min(MAX_DIRT, currentDirt + newDirt)

    def updateDirt(self, useRobotMap=False):
        # Updates dirt by adding more based on however much is there to begin with and the adjacent cells
        #Todo: seeding
        import random

        mapCopy = self.copy(copyMap = True) #Check copy so dirt doesn't cascade across the map from earlier checks


        for y in xrange(0,int(mapCopy.yCells-1)):
            for x in xrange(0,int(mapCopy.xCells-1)):

                if mapCopy.map[x][y].isObstacle:
                    #Obstacle that can't be cleaned
                    continue

                elif mapCopy.map[x][y].value == None:
                    #It's a cell not in the environment
                    continue


                elif mapCopy.map[x][y].label == None or mapCopy.map[x][y].label == '' or mapCopy.map[x][y].label == 'None':
                    randomVal = random.random()
                    cellDist = openCellDist[str(mapCopy.map[x][y].dirt)]
                    
                    #Own cell: default dirt generation
                    if randomVal < cellDist[0]:
                        self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)
                

                else:
                    #Own cell: Generation based on label
                    randomVal = random.random()
                    labelDist = labelDict[str(mapCopy.map[x][y].label)]
                    cellDist = labelDist[str(mapCopy.map[x][y].dirt)]
                    if randomVal < cellDist[0]:
                        self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)


                #for i in mapCopy.adjacent(x, y):
                #    print i.dirt, i.isObstacle, i.isVisited, i.label, i.value

                #Dirt generation from adjacent cells
                for cell in mapCopy.adjacent(x, y):
                    if cell.isObstacle:
                        #print "Skipping: obstacle"
                        continue

                    elif cell.value == None:
                        #print "Skipping: none cell value"
                        continue

                    elif cell.label == None or (cell.label == 'None'):
                        randomVal = random.random()
                        cellDist = openCellDist[str(cell.dirt)]
                        #print "No cell label", x, y, cellDist, randomVal, randomVal < cellDist[1], self.map[x][y].dirt, self.map[x][y].value
                    
                        #Adjacent cell: default dirt generation
                        if randomVal < cellDist[1]:
                            self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)

                    else:
                        #print "Cell label"
                        #Adjacent cell: Generation based on label
                        randomVal = random.random()
                        labelDist = labelDict[str(mapCopy.map[x][y].label)]
                        cellDist = labelDist[str(mapCopy.map[x][y].dirt)]
                        if randomVal < cellDist[1]:
                            self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)

                self.map[x][y].value = self.map[x][y].dirt


    def autoClassify( self, environment ):
        #take in an environment and copy in the labels
        
        mapcp = self.copy()

        for x in xrange(0,int(mapcp.xCells)):
            for y in xrange(0,int(mapcp.yCells)):
                #map              environments "map"
                mapcp.map[x][y].label = environment.map[x][y].label

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
        self.map = [[MapNode(rows, columns) for columns in xrange(self.width/cellXSize)] for rows in xrange(self.height/cellYSize)]


        self.importEnviroment(environmentCSV)

    def get_dirt(self):
        """Give back coordinates of dirt in the environment's map"""
        dirt_cells = []
        for row in range(self.heightCells):
            for col in range(self.widthCells):
                if self.map[row][col].dirt > 0:
                    dirt_cells.append((col, row))
        return dirt_cells

    def copy (self):
        mapcp = Environment()

        cellXMax = self.width/self.cellXSize
        cellYMax = self.height/self.cellYSize

        for x in xrange(0,int(cellXMax)):
            for y in xrange(0,int(cellYMax)):
                mapcp.map[x][y] = self.map[x][y].copy(y,x)

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

    def addDirt(self, currentDirt, newDirt):
        # Returns amount of dirt after adding newDirt to currentDirt
        return min(MAX_DIRT, currentDirt + newDirt)

    def updateDirt(self, useRobotMap=False):
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
                    #It's a cell not in the environment
                    continue


                elif mapCopy.map[x][y].label == None or mapCopy.map[x][y].label == '':
                    randomVal = random.random()
                    cellDist = openCellDist[str(mapCopy.map[x][y].dirt)]
                    
                    #Own cell: default dirt generation
                    if randomVal < cellDist[0]:
                        self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)
                

                else:
                    #Own cell: Generation based on label
                    #print "cell label: ",(mapCopy.map[x][y].label)
                    randomVal = random.random()
                    labelDist = labelDict[str(mapCopy.map[x][y].label)]
                    cellDist = labelDist[str(mapCopy.map[x][y].dirt)]
                    if randomVal < cellDist[0]:
                        self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)


                #for i in mapCopy.adjacent(x, y):
                #    print i.dirt, i.isObstacle, i.isVisited, i.label, i.value

                #Dirt generation from adjacent cells
                for cell in mapCopy.adjacent(x, y):
                    if cell.isObstacle:
                        #print "Skipping: obstacle"
                        continue

                    elif cell.value == None:
                        #print "Skipping: none cell value"
                        continue

                    elif cell.label == None:
                        randomVal = random.random()
                        cellDist = openCellDist[str(cell.dirt)]
                        #print "No cell label", x, y, cellDist, randomVal, randomVal < cellDist[1], self.map[x][y].dirt, self.map[x][y].value
                    
                        #Adjacent cell: default dirt generation
                        if randomVal < cellDist[1]:
                            self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)

                    else:
                        #print "Cell label"
                        #Adjacent cell: Generation based on label
                        randomVal = random.random()
                        labelDist = labelDict[str(mapCopy.map[x][y].label)]
                        cellDist = labelDist[str(mapCopy.map[x][y].dirt)]
                        if randomVal < cellDist[1]:
                            self.map[x][y].dirt = self.addDirt(self.map[x][y].dirt, 1)

                self.map[x][y].value = self.map[x][y].dirt

    def importEnviroment(self,csvFile):

        with open(csvFile,'r') as csvFile:
            i = 0
            j = 0
            reader = csv.reader(csvFile)
            for row in reader:
                for column in row:
                    if i > ((self.width/self.cellXSize)-1):
                        break
                    if(column != ''):
                        if '"' in column:
                            print column
                            print i
                            print j
                
                            column = column.replace('[','')
                            column = column.replace(']','')
                            column = column.replace('"','')
                            column = column.replace('"','')
                            column = column.split(',')

                            value = int(column[0])
                            if value >= 0:
                                if value > 3:
                                    value = 3
                                self.map[i][j].dirt = value
                            else:
                                self.map[i][j].isObstacle = True

                            print column
                            self.map[i][j].value = int(column[0])
                            self.map[i][j].label = str(column[1])
                            #print self.map[i][j].label

                        if '[' in column:
                            column = column.replace('[','')
                            column = column.replace(']','')
                            column = column.split(',')

                            value = int(column[0])
                            if value >= 0:
                                if value > 3:
                                    value = 3
                                self.map[i][j].dirt = value
                            else:
                                self.map[i][j].isObstacle = True

                            self.map[i][j].value = int(column[0])
                            self.map[i][j].label = str(column[1])
                            #print self.map[i][j].label
                        else:
                            
                            value = int(column)
                            if value >= 0:
                                if value > 3:
                                    value = 3
                                self.map[i][j].dirt = value
                            else:
                                self.map[i][j].isObstacle = True
                            self.map[i][j].value = int(column)
                    else:
                        self.map[i][j].value = None
                    i += 1
                i = 0
                j += 1

                if j > ((self.height/self.cellYSize)-1):
                    break
            return
                
    @staticmethod
    def generateMapOrientations(m):
        orient = list()
        orient.append(list(m))
        orient.append(Environment.rotateMap(orient[0]))
        orient.append(Environment.rotateMap(orient[1]))
        orient.append(Environment.rotateMap(orient[2]))
        orient.append(Environment.flipMap(orient[0]))
        orient.append(Environment.flipMap(orient[1]))
        orient.append(Environment.flipMap(orient[2]))
        orient.append(Environment.flipMap(orient[3]))
        return orient

    @staticmethod
    def rotateMap(m, width = 10, height = 10):
        mcp = list(m)
        if width != height:
            print "Can't do that"
        else:
            for x in range(0, int(width)):
                for y in range(0, int(height)):
                    mcp[y][width - 1 - x] = m[x][y]
            return mcp
    @staticmethod
    def flipMap(m, width = 10, height = 10):
        mcp = list(m)
        if width != height:
            print "Can't do that"
        else:
            for x in range(0, int(width)):
                for y in range(0, int(height)):
                    mcp[x][height - 1 - y] = m[x][y]
            return

    def copyEnvIntoMap( self, m ):
        #Takes in a map, and ports the environment into the map 
        #as if the robot fully explored it.

        mapcp = m.copy()
        mapcp.dirtCells = []
        mapcp.visitedCells = []
        mapcp.unvisitedCells = []
        mapcp.obstacles = []
        mapcp.robotPositions = []

        self.unvisitedCells = []
        
        for x in xrange(0,int(mapcp.xCells)):
            for y in xrange(0,int(mapcp.yCells)):
                #map              environments "map"
                mapcp.map[x][y] = self.map[x][y].copy(y,x)
                mapcp.map[x][y].label = None 


                if self.map[x][y].value > 0:
                    mapcp.dirtCells.append([x,y,self.map[x][y].value])

                if self.map[x][y].value == -1:
                    mapcp.obstacles.append([x,y])

                if self.map[x][y].value == 0:
                    mapcp.map[x][y].isVisited = True


        #print mapcp.visitedCells 
        return mapcp
