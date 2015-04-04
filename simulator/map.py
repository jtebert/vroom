
import time
import pygame
from pygame. locals import *
from math import ceil, floor, atan2, degrees, radians, sqrt
import csv

class Node(object):
    
    def __init__(self):
        self.isObstacle = False
        self.isVisited = False
        self.dirt = -1
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

        self.map = [[Node() for columns in xrange(self.width/cellXSize)] for rows in xrange(self.height/cellYSize)]

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
                    if environment.map[y][x].value == -1:
                        pygame.draw.rect(screen,(0,0,0),r,0)
                    elif environment.map[y][x].value == 0:
                        pygame.draw.rect(screen,(255,255,255),r,0)
                    elif environment.map[y][x].value > 0:
                        d = environment.map[y][x].value
                        pygame.draw.rect(screen,(0,0,255-(40*d)),r,0)

                else:
                    if self.map[y][x].isObstacle:
                        pygame.draw.rect(screen,(0,0,0),r,0)
                    elif (self.map[y][x].dirt > 0):
                        d = self.map[y][x].dirt
                        pygame.draw.rect(screen,(0,0,255-(40*d)),r,0)
                    elif self.map[y][x].isVisited:
                        pygame.draw.rect(screen,(255,255,255),r,0)


    def drawRobot (self,screen,robot):


        for x in range(-2,3,1):
            for y in range (-2,3,1):
                self.map[robot.pos[1]+x][robot.pos[0]+y].isVisited = True

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


class Environment(object):
    center = (0,0)


    def __init__(self,w=700,h=700,cellXSize=10,cellYSize=10):
        self.cellXSize = cellXSize
        self.cellYSize = cellYSize
        self.width = w
        self.height = h
        self.boundingBox = ((w/2,h/2),(w/2,h/2))
        self.map = [[Node() for columns in xrange(self.width/cellXSize)] for rows in xrange(self.height/cellYSize)]


        self.importEnviroment('./../assets/maps/test.csv')


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
                            self.map[i][j].value = int(column[0])
                            self.map[i][j].label = column[1]
                        else:
                            self.map[i][j].value = int(column)



                    j += 1
                j = 0
                i += 1

                if i > (self.height/self.cellYSize):
                    break
            return
                
    
    
