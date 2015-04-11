from map import *

import os,sys,inspect, getopt


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from explore_map import *

import time

class RobotSimulator(object):

    def __init__(self, inputEnv):
            
        
        # the world
        self.environment = Environment(environmentCSV=inputEnv)

        # what the robot knows
        self.map = RobotMap()

        # the robot needs the environment so the sensors can reference it for readings
        self.robot = Robot(self.environment)

        self.showEnvironment = False
        self.k = None
        self.action = None

        self.start = False
        self.updateDirt = False

        
    
    def listenControls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return 

            
            if event.type == pygame.KEYDOWN:
                self.k=event.key
            if event.type == pygame.KEYUP:
                self.k = None
                self.action = 'None'
            if self.k != None:
                if self.k == pygame.K_q:
                    self.start = True
                if self.k == pygame.K_UP:
                    self.action = 'North'
                if self.k == pygame.K_DOWN:
                    self.action = 'South'
                if self.k == pygame.K_RIGHT:
                    self.action = 'East'
                if self.k == pygame.K_LEFT:
                    self.action = 'West'
                if self.k == pygame.K_e:
                    self.showEnvironment = (not self.showEnvironment)
                if self.k == pygame.K_d:
                    self.updateDirt = True
            




    def run(self):
        
        pygame.init()
        pygame.display.set_mode((700,700),pygame.RESIZABLE)
        pygame.display.update()

        self.turning = False
        self.turningDistance = 0
        self.turnDirection = None
        self.bump = None
        self.cleanDirection = 'Down'

        state = RobotState(self.robot,self.map )
        agent = None  #TODO replace with agent selection

        
        #TODO defaults to run exploration and then shows results
        problem = MapEnvironmentProblem(state, 70)
        heuristic = exploration_heuristic
        #actions = depth_first_search(problem)
        

        while(True):

            
            if (agent == None):
                self.listenControls()

                if self.updateDirt:
                    self.updateDirt = False
                    self.environment.updateDirt()
                #self.action is set directly by self.listenControls
            else:
                self.action = agent.getAction(state)
            
            
            '''
            if len(actions):
                self.action = actions.pop(0)
            else:
                self.action = 'None'
            '''    
                
            screen = pygame.display.get_surface()

            state = state.generateSuccessor(self.action)
            
            #update Screen
            screen.fill((204,204,204))  
            
            if self.showEnvironment:
                state.map.draw(screen,environment = self.environment)
                state.map.drawRobot(screen,state.r)
            else:
                state.map.draw(screen)
                state.map.drawRobot(screen,state.r)
            

            
            pygame.display.update()


        

class Robot(object):

    def __init__(self,environment, pos=[5,4],heading='East'):

        self.size = 50   #5x5 cells
        self.pos = [5,4]
        self.heading = heading
        self.environment = environment

    def proximitySensor(self):
        #checks immediate surroundings for obstacles

        #TODO This assumes a robot size of 5, make it adaptable
        
        pos = self.pos
        
        obsLocations = []
        openLocations = []


        #check for sides
        for i in range(-2,3,1):

            if self.environment.map[pos[0]-3][pos[1]+i].value == -1:
                obsLocations.append([pos[0]-3,pos[1]+i])
            else:
                openLocations.append([pos[0]-3,pos[1]+i])

            if self.environment.map[pos[0]+3][pos[1]+i].value == -1:
                obsLocations.append([pos[0]+3,pos[1]+i])
            else:
                openLocations.append([pos[0]+3,pos[1]+i])

            if self.environment.map[pos[0]+i][pos[1]+3].value == -1:
                obsLocations.append([pos[0]+i,pos[1]+3])
            else:
                openLocations.append([pos[0]+i,pos[1]+3])

            if self.environment.map[pos[0]+i][pos[1]-3].value == -1:
                obsLocations.append([pos[0]+i,pos[1]-3])
            else:
                openLocations.append([pos[0]+i,pos[1]-3])

        #check for corners        
        if self.environment.map[pos[0]-3][pos[1]-3].value == -1:
            obsLocations.append([pos[0]-3,pos[1]-3])
        else:
            openLocations.append([pos[0]-3,pos[1]-3])

        if self.environment.map[pos[0]-3][pos[1]+3].value == -1:
            obsLocations.append([pos[0]-3,pos[1]+3])
        else:
            openLocations.append([pos[0]-3,pos[1]+3])

        if self.environment.map[pos[0]+3][pos[1]-3].value == -1:
            obsLocations.append([pos[0]+3,pos[1]-3])
        else:
            openLocations.append([pos[0]+3,pos[1]-3])

        if self.environment.map[pos[0]+3][pos[1]+3].value == -1:
            obsLocations.append([pos[0]+3,pos[1]+3])
        else:
            openLocations.append([pos[0]+3,pos[1]+3])
        

        return obsLocations,openLocations
        

    def bumpSensor(self, action):
        b = []
        
        bumpCoordinates = self.getBumpCoordinates(action)

        if bumpCoordinates != None:
            for pos in bumpCoordinates:
                if self.environment.map[pos[0]][pos[1]].value == -1:
                    b.append(pos)
        return b

    def isBump(self, bumpSensor):
        bump = False
        if len(bumpSensor):
            bump = True
        return bump

    def getBumpCoordinates(self, action):
        
        coords = None
        
        if self.heading == action:
            if action == 'North':
                coords = [[self.pos[0],self.pos[1]-3], 
                          [self.pos[0]-1,self.pos[1]-3],
                          [self.pos[0]+1,self.pos[1]-3],
                          [self.pos[0]-2,self.pos[1]-3],
                          [self.pos[0]+2,self.pos[1]-3]]

            if action == 'South':
                coords = [[self.pos[0]+1,self.pos[1]+3],
                          [self.pos[0],self.pos[1]+3], 
                          [self.pos[0]-1,self.pos[1]+3],
                          [self.pos[0]-2,self.pos[1]+3],
                          [self.pos[0]+2,self.pos[1]+3]]

            if action == 'East':
                coords = [[self.pos[0]+3,self.pos[1]], 
                          [self.pos[0]+3,self.pos[1]-1],
                          [self.pos[0]+3,self.pos[1]+1],
                          [self.pos[0]+3,self.pos[1]-2],
                          [self.pos[0]+3,self.pos[1]+2]]

            if action == 'West':
                coords = [[self.pos[0]-3,self.pos[1]], 
                          [self.pos[0]-3,self.pos[1]-1],
                          [self.pos[0]-3,self.pos[1]+1],
                          [self.pos[0]-3,self.pos[1]-2],
                          [self.pos[0]-3,self.pos[1]+2]]

        return coords

    def getEmptySpaceCoords(self, action):
        coords = []
        
        if self.heading == action:
            if action == 'North':
                coords = [[self.pos[0],self.pos[1]-3], 
                          [self.pos[0]-1,self.pos[1]-3],
                          [self.pos[0]+1,self.pos[1]-3],
                          [self.pos[0]-2,self.pos[1]-3],
                          [self.pos[0]+2,self.pos[1]-3]]

            if action == 'South':
                coords = [[self.pos[0]+1,self.pos[1]+3],
                          [self.pos[0],self.pos[1]+3], 
                          [self.pos[0]-1,self.pos[1]+3],
                          [self.pos[0]-2,self.pos[1]+3],
                          [self.pos[0]+2,self.pos[1]+3]]

            if action == 'East':
                coords = [[self.pos[0]+3,self.pos[1]], 
                          [self.pos[0]+3,self.pos[1]-1],
                          [self.pos[0]+3,self.pos[1]+1],
                          [self.pos[0]+3,self.pos[1]-2],
                          [self.pos[0]+3,self.pos[1]+2]]

            if action == 'West':
                coords = [[self.pos[0]-3,self.pos[1]], 
                          [self.pos[0]-3,self.pos[1]-1],
                          [self.pos[0]-3,self.pos[1]+1],
                          [self.pos[0]-3,self.pos[1]-2],
                          [self.pos[0]-3,self.pos[1]+2]]

        return coords
        

    def dirtSensor(self):
        dValues = []

        #the whole robot is a vacuum!
        for x in range(-2,3,1):
            for y in range (-2,3,1): 
            
                if self.environment.map[self.pos[0]+x][self.pos[1]+y].value > 0:
                    d = self.environment.map[self.pos[0]+x][self.pos[1]+y].value
                    dValues.append([self.pos[0]+x,self.pos[1]+y,d])
        
        return dValues


    def takeAction(self,action):
        
        

        if (self.heading == action):
            #drive forwards
            if action == 'North':
                #north is negative
                self.pos[1] -= 1
            if action == 'East':
                self.pos[0] += 1
            if action == 'West':
                self.pos[0] -= 1
            if action == 'South':
                self.pos[1] += 1
                
        else:
            #turn torwards requested action
            self.heading = self.evaluateTurn(action)

        #print "robot pos: ",self.pos
        #print "robot heading: ",self.heading

    def evaluateTurn(self,action):
        
        heading = self.heading

        if self.heading == 'None':
            heading = action

        if self.heading == 'North':
            if (action == 'East') or (action == 'TurnRight'):
                heading = 'East'
            if (action == 'West') or (action == 'TurnLeft'):
                heading = 'West'

        if self.heading == 'East':
            if (action == 'South') or (action == 'TurnRight'):
                heading = 'South'
            if (action == 'North') or (action == 'TurnLeft'):
                heading = 'North'

        if self.heading == 'South':
            if (action == 'West') or (action == 'TurnRight'):
                heading = 'West'
            if (action == 'East') or (action == 'TurnLeft'):
                heading = 'East'
                
        if self.heading == 'West':
            if (action == 'North') or (action == 'TurnRight'):
                heading = 'North'
            if (action == 'South') or (action == 'TurnLeft'):
                heading = 'South'

        return heading


    def copy(self):
        r = Robot(self.environment)
        r.pos = self.pos
        r.heading = self.heading
        return r

class RobotState:


    def getLegalActions( self ):

        possibleActions = ['North','South','East','West','None']
        legalActions = []

        for action in possibleActions:
            bumpReadings = self.r.bumpSensor(action)
            if (len(bumpReadings) == 0):
                legalActions.append(action)
        
        return legalActions

    def proxSensorCoords (self, action):
        # For a given action, return the coordinates of the proximety sensor
        # at that position
        coords = []
        pos = list(self.r.pos)
        

        if self.r.heading == action:
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
                
        

    def willVisitNewCell( self, action):
        cellCoords = self.r.getEmptySpaceCoords(action)
        result = False

        unvisitedCells = self.getUnvisited()
        
        for coord in cellCoords:
            if ((coord) in unvisitedCells):
                result = True

        return result

    def generateSuccessor( self, action ):
        
        #create copy of the current state
        #need to make a copy of the map
        #does the environment need to be coppied?
        robotCp = self.r.copy()
        mapCp = self.map.copy()
        state = RobotState(robotCp, mapCp )
       
        #print self.willVisitNewCell(action)
        #print self.willExploreNewCell(action)
        
        if action != None:
            #check bumper 
            bumpReadings = state.r.bumpSensor(action)
            proxReadings,openReadings = state.r.proximitySensor()
            dirtReadings = state.r.dirtSensor()
            
            if len(dirtReadings):
                for dirtReading in dirtReadings:
                    state.map.map[dirtReading[0]][dirtReading[1]].dirt = dirtReading[2]
                    if (dirtReading not in state.map.dirtCells):
                        state.map.dirtCells.append(dirtReading)
                
            if len(proxReadings):
                for prox in proxReadings:
                    state.map.map[prox[0]][prox[1]].isObstacle = True
                    
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

                
        return state

    def getRobotPosition( self ):
        
        return self.r.pos
        
    def getDirt( self ):

        return self.map.dirtCells

    def getUnvisited( self ):
        return self.map.unvisitedCells

    def getVisited( self ):
        return self.map.visitedCells

    def getObserved ( self ):
        return self.map.observedCells

    def getObstacles( self ):
        return self.map.obstacles

    def __init__ ( self, robot , robotMap ):

        self.r = robot
        self.map = robotMap

if __name__ == "__main__":
    
    #TODO add option to import environment
    #TODO add option for real vs simulated robot
    
    try: 
        opts,args = getopt.getopt(sys.argv[1:],"ie:")
    except getopt.GetoptError:
        print "robot.py -e <environmentPath>"
        sys.exit(2)
        

    defaultEnvironmentCSV = './../assets/maps/test.csv'
    saveMapEnvAtEnd = False
    for opt,arg in opts:
        if opt == '-e':
            defaultEnvironmentCSV = arg
        if opt == '-i':
            saveMapEnvAtEnd = True


    r = RobotSimulator(defaultEnvironmentCSV)

    if saveMapEnvAtEnd:
        try:
            r.run()
        except:
                    
            screen = pygame.display.get_surface()
            #update Screen
            screen.fill((204,204,204))  
            r.map.draw(screen,environment = r.environment)
            r.map.drawRobot(screen,r.robot)

            pygame.image.save(screen, './endEnvironment.jpg')

            #update Screen
            screen.fill((204,204,204))  
   
            r.map.draw(screen)
            r.map.drawRobot(screen,r.robot)
            
            pygame.image.save(screen, './endMap.jpg')
            

    else:
        r.run()
