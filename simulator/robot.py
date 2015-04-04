
from map import *

import time

class RobotSimulator(object):

    def __init__(self):

        # what the robot knows
        self.map = RobotMap()
        
        # the world
        self.environment = Environment()
        self.robot = Robot(self.environment)

        self.showEnvironment = False
        self.k = None
        self.action = None

        self.start = False

        
    
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
            




    def run(self):
        
        pygame.init()
        pygame.display.set_mode((700,700),pygame.RESIZABLE)
        pygame.display.update()

        self.turning = False
        self.turningDistance = 0
        self.turnDirection = None
        self.bump = None
        self.cleanDirection = 'Down'

        state = RobotState(self.robot,self.map, self.environment)
        agent = None  #TODO replace with agent selection

        while(True):

            if (agent == None):
                self.listenControls()
                #self.action is set directly by self.listenControls
            else:
                self.action = agent.getAction(state)
                
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

    def __init__(self,environment):

        self.size = 50   #5x5 cells
        self.pos = [5,4]
        self.heading = 'East'
        self.environment = environment

    def proximitySensor(self):
        #checks immediate surroundings for obstacles

        #TODO This assumes a robot size of 5, make it adaptable
        
        pos = self.pos
        
        obsLocations = []


        #check for sides
        for i in range(-2,3,1):
            if self.environment.map[pos[1]-3][pos[0]+i].value == -1:
                obsLocations.append([pos[0]+i,pos[1]-3])
            if self.environment.map[pos[1]+3][pos[0]+i].value == -1:
                obsLocations.append([pos[0]+i,pos[1]+3])
            if self.environment.map[pos[1]+i][pos[0]+3].value == -1:
                obsLocations.append([pos[0]+3,pos[1]+i])
            if self.environment.map[pos[1]+i][pos[0]-3].value == -1:
                obsLocations.append([pos[0]-3,pos[1]+i])

        #check for corners        
        if self.environment.map[pos[1]-3][pos[0]-3].value == -1:
            obsLocations.append([pos[0]-3,pos[1]-3])
        if self.environment.map[pos[1]-3][pos[0]+3].value == -1:
            obsLocations.append([pos[0]+3,pos[1]-3])
        if self.environment.map[pos[1]+3][pos[0]-3].value == -1:
            obsLocations.append([pos[0]-3,pos[1]+3])
        if self.environment.map[pos[1]+3][pos[0]+3].value == -1:
            obsLocations.append([pos[0]+3,pos[1]+3])

        return obsLocations
        

    def bumpSensor(self, action):
        b = []
        
        bumpCoordinates = self.getBumpCoordinates(action)

        if bumpCoordinates != None:
            for pos in bumpCoordinates:
                if self.environment.map[pos[1]][pos[0]].value == -1:
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
            
        

    def dirtSensor(self):
        dValues = []

        #the whole robot is a vacuum!
        for x in range(-2,3,1):
            for y in range (-2,3,1): 
            
                if self.environment.map[self.pos[1]+x][self.pos[0]+y].value > 0:
                    d = self.environment.map[self.pos[1]+x][self.pos[0]+y].value
                    dValues.append([self.pos[0]+y,self.pos[1]+x,d])
        
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


class RobotState:


    def getLegalActions( self ):

        possibleActions = ['North','South','East','West','None']
        legalActions = []

        for action in possibleActions:
            bumpReadings = self.r.bumpSensor(action)
            if (len(bumpReadings) == 0):
                legalActions.append(action)
        
        return legalActions

    def generateSuccessor( self, action ):
        
        #create copy of the current state
        state = RobotState(self.r, self.map, self.r.environment)

        actions = self.getLegalActions()

        #TODO need a reference to the environment for the sensors
        if action != None:
            #check bumper 
            bumpReadings = state.r.bumpSensor(action)
            proxReadings = state.r.proximitySensor()
            dirtReadings = state.r.dirtSensor()
            
            if len(dirtReadings):
                for dirtReading in dirtReadings:
                    state.map.map[dirtReading[1]][dirtReading[0]].dirt = dirtReading[2]
                    if (dirtReading not in state.map.dirtCells):
                        state.map.dirtCells.append(dirtReading)
                
            if len(proxReadings):
                for prox in proxReadings:
                    state.map.map[prox[1]][prox[0]].isObstacle = True
                    
                    if (prox not in state.map.obstacles):
                        state.map.obstacles.append(prox)

            if(not(state.r.isBump(bumpReadings))):
                state.r.takeAction(action)
            else:
                self.bump = True

        dirt = self.getDirt()
        print dirt
                
        return state

    def getRobotPosition( self ):
        
        return self.r.pos
        
    def getDirt( self ):

        return self.map.dirtCells

    def getUnvisited( self ):
        return self.map.unvisitedCells

    def getVisited( self ):
        return self.map.visitedCells

    def getObstacles( self ):
        return self.map.obstacles

    def __init__ ( self, robot , robotMap , environment):

        self.r = robot
        self.r.environment
        self.map = robotMap

if __name__ == "__main__":
    
    #TODO add option to import environment
    #TODO add option for real vs simulated robot

    r = RobotSimulator()
    r.run()
