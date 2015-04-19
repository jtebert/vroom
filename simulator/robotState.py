

class RobotState:

    def __init__ ( self, robot , robotMap ):
            
        self.r = robot
        self.map = robotMap

    def resetMission (self ):
        #swap unvisited with visited

        temp = self.map.unvisitedCells

        #print "old unvisited: ",self.map.unvisitedCells
        #print "old visited: ",self.map.visitedCells

        self.map.unvisitedCells = []
        self.map.unvisitedCells = list(self.map.visitedCells)
        self.map.visitedCells = list(temp)

        #print "new unvisited : ",self.map.unvisitedCells
        #print "new visited : ",self.map.visitedCells

        return self

    def getLegalActions( self, pos):

        possibleActions = ['North','East','South','West','None']
        legalActions = []

        for action in possibleActions:
            bumpReadings = self.r.bumpSensor(action, position=pos)
            if (len(bumpReadings) == 0):
                legalActions.append(action)

        return legalActions

    def proxSensorCoords (self, action):
        # For a given action, return the coordinates of the proximity sensor
        # at that position
        coords = []
        pos = list(self.r.pos)


        if action == 'North':
            pos[1] -= 1
        if action == 'South':
            pos[1] += 1
        if action == 'East':
            pos[0] += 1
        if action == 'West':
            pos[0] -= 1


        for i in range(-2,3,1):
            coords.append([pos[0]-3,pos[1]+i])
            coords.append([pos[0]+3,pos[1]+i])
            coords.append([pos[0]+i,pos[1]-3])
            coords.append([pos[0]+i,pos[1]+3])

        #dont forget the corners :-)
        coords.append([pos[0]+3,pos[1]+3])
        coords.append([pos[0]-3,pos[1]+3])
        coords.append([pos[0]+3,pos[1]-3])
        coords.append([pos[0]-3,pos[1]-3])

        return coords

    def willExploreNewCell (self, action):
        #if the robot will explore a new cell return true

        coords = self.proxSensorCoords(action)
        observedCells = self.getObserved()
        result = False

        #print observedCells

        for coord in coords:
            if coord in observedCells:
                result = True

        return result



    def willVisitNewCell( self, pos, action):
        cellCoords = self.r.getBumpCoordinates(action, pos)
        result = 0

        unvisitedCells = self.getUnvisited()
        #print len(unvisitedCells)

        for coord in cellCoords:
            if (coord in unvisitedCells):
                result += 1

        return result


    def generateSuccessor( self, action ):

        #create copy of the current state
        #need to make a copy of the map
        #does the environment need to be copied?
        robotCp = self.r.copy()
        mapCp = self.map.copy()
        state = RobotState(robotCp, mapCp )

        #print self.getLegalActions(self.r.pos)
        #print self.willVisitNewCell(self.r.pos, action)

        #print "start generate successor: ",action
        #print "position: ",state.r.pos

        if action != None:
            #check bumper
            bumpReadings = state.r.bumpSensor(action)
            proxReadings,openReadings = state.r.proximitySensor()
            dirtReadings = state.r.dirtSensor()

            if len(dirtReadings):
                for dirtReading in dirtReadings:
                    state.map.map[dirtReading[0]][dirtReading[1]].dirt = dirtReading[2]
                    state.map.map[dirtReading[0]][dirtReading[1]].value = dirtReading[2]
                    state.r.environment.map[dirtReading[0]][dirtReading[1]].dirt = 0
                    if (dirtReading not in state.map.dirtCells):
                        state.map.dirtCells.append(dirtReading)

            if len(proxReadings):
                for prox in proxReadings:
                    state.map.map[prox[0]][prox[1]].isObstacle = True
                    state.map.map[prox[0]][prox[1]].value = -1 

                    if (prox not in state.map.obstacles):
                        state.map.obstacles.append(prox)

                    if (prox in state.map.unvisitedCells):
                        state.map.unvisitedCells.remove(prox)

            #print "length of openreadings: ",len(openReadings)
            if len(openReadings):
                for openCell in openReadings:

                    if openCell in state.map.unvisitedCells:
                       # print "adding observed cell: ",openCell
                        state.map.observedCells.append(openCell)

            if(not(state.r.isBump(bumpReadings))):
                state.r.takeAction(action)
            else:
                self.bump = True

            pos = [0,0]
            pos[0] = int(state.r.pos[0])
            pos[1] = int(state.r.pos[1])
            for x in range(-2,3,1):
                for y in range (-2,3,1):
                    state.map.map[pos[0]+x][pos[1]+y].isVisited = True
                    state.map.map[pos[0]+x][pos[1]+y].value = 0

                    if ([pos[0]+x,pos[1]+y] not in state.map.visitedCells):
                        state.map.visitedCells.append([pos[0]+x,pos[1]+y])

                    if ([pos[0]+x,pos[1]+y] in state.map.observedCells):
                        state.map.observedCells.remove([pos[0]+x,pos[1]+y])

                    if ([pos[0]+x,pos[1]+y] in state.map.unvisitedCells):
                        state.map.unvisitedCells.remove([pos[0]+x,pos[1]+y])

            if pos not in (state.map.robotPositions):
                state.map.robotPositions.append([pos[0],pos[1]])

        #print "end generate successor: ",state.r.pos

        return state

    def extractSmallState ( self ):
        #return the only state needed for the search problem
        dirt = self.getDirt()
        pos = (self.r.pos[0],self.r.pos[1])
        state = (pos, len(dirt))
        return state

    def getRobotPosition( self ):

        return self.r.pos

    def getDirt( self ):

        removeList = []

        for dirtCell in self.map.dirtCells:
            pos = [dirtCell[0],dirtCell[1]]
            if pos in self.map.visitedCells:
                removeList.append(dirtCell)

        dirt = list(self.map.dirtCells)

        for cell in removeList:
            dirt.remove(cell)

        return dirt

    def clearDirt( self ):
        for x in xrange(0,int(self.map.xCells)):
            for y in xrange(0,int(self.map.yCells)):
                if self.map.map[x][y].value > 0:
                    self.map.map[x][y].value = 0
                self.map.map[x][y].dirt = 0
        

    def removeUnreachableDirt ( self ):
        #after performing update dirt, or if importing a map with dirt cells
        #we will need to remove dirtCells from the dirt list the robot cannot
        #reach
        dirt = self.getDirt()

        for cell in dirt:
            pos = [dirt[0],dirt[1]]
            if pos not in self.getVisited():
                #unreachable dirt, remove it
                dirt.remove(cell)

        self.map.dirtCells = list(dirt)
        return 

    def getUnvisited( self ):
        return self.map.unvisitedCells

    def getVisited( self ):
        return self.map.visitedCells

    def getObserved ( self ):
        return self.map.observedCells

    def getObstacles( self ):
        return self.map.obstacles

    def copy( self ):
        robotCp = self.r.copy(copyEnv=True)
        mapCp = self.map.copy(copyMap=True)
        stateCp = RobotState(robotCp, mapCp )
        return stateCp

    def featureExtraction(self, inputMap, classifiers):

        # to start with, just uses every blocksize x blocksize section
        blockSize = 10
        #print "xCells:", inputMap.xCells, "yCells:", inputMap.yCells, "blockSize", blockSize
        xRange = int(inputMap.xCells - blockSize + 1)
        yRange = int(inputMap.yCells - blockSize + 1)
        #print "xRange:", xRange, "yRange:", yRange
        for y in xrange(0, yRange):
            for x in xrange(0, xRange):
                print "fE", x, y
                # Run classifier on block
                # Limits of this block are [x, x+blockSize] and [y, y+blockSize]
                map = inputMap.map
                submatrix = [[map[i][j].value for i in range(x, x+blockSize)] for j in range(y, y+blockSize)]

                bestClassifier = classifiers.getBestClassifier(submatrix)
                print "best classifier:", bestClassifier
                if bestClassifier != None:
                    for a in xrange(y, y + blockSize):
                        for b in xrange(x, x + blockSize):
                            map[b][a].label = bestClassifier
                            #print "fe updatelabel", a, b
