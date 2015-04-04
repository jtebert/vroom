
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

        #time.sleep(15)
        

        '''
        while(not self.start):
            self.listenControls()
        '''


        while(True):
            self.listenControls()
            screen = pygame.display.get_surface()

            '''
            time.sleep(0.05)

            bumpReadings = self.robot.bumpSensor(self.robot.heading,self.environment)
            if (self.bump and (not self.turning)):
                self.bump = False
                self.turning = True
                self.turningDistance = 0

                if (self.cleanDirection == 'Down'):
                    if(self.robot.heading == 'East'):
                        self.action = "TurnRight"
                        self.turnDirection = self.action
                    else: 
                        self.action = "TurnLeft"
                        self.turnDirection = self.action
                else:
                    if(self.robot.heading == 'East'):
                        self.action = "TurnLeft"
                        self.turnDirection = self.action
                    else: 
                        self.action = "TurnRight"
                        self.turnDirection = self.action

            elif ((self.turningDistance == 5)):
                self.action = self.turnDirection
                self.turningDistance = 0
                self.turning = False
            elif (self.turning):
                if (self.bump):
                    
                    print "bumped while turning!: ,",self.turningDistance
                    if (self.turningDistance <= 2):
                        print "changing cleaning direction!"
                        if self.cleanDirection == 'Down':
                            self.cleanDirection == 'Up'

                    self.action = self.turnDirection
                    self.turningDistance = 0
                    self.turning = False
                    self.bump = False
                else:
                    self.turningDistance += 1
                    self.action = self.robot.heading

            else:
                self.action = self.robot.heading
            
            '''

            if self.action != None:
                #check bumper 
                bumpReadings = self.robot.bumpSensor(self.action,self.environment)
                proxReadings = self.robot.proximitySensor(self.environment)
                dirtReadings = self.robot.dirtSensor(self.environment)

                if len(dirtReadings):
                    for dirtReading in dirtReadings:
                        self.map.map[dirtReading[1]][dirtReading[0]].dirt = dirtReading[2]

                if len(proxReadings):
                    for prox in proxReadings:
                        self.map.map[prox[1]][prox[0]].isObstacle = True

                if(not(self.robot.isBump(bumpReadings))):
                    self.robot.takeAction(self.action)
                else:
                    self.bump = True
                    
                self.action = None
            


            screen.fill((204,204,204))  
            
            if self.showEnvironment:
                self.map.draw(screen,environment = self.environment)
                self.map.drawRobot(screen,self.robot)
            else:
                self.map.draw(screen)
                self.map.drawRobot(screen,self.robot)
            

            
            pygame.display.update()


        

class Robot(object):

    def __init__(self,environment):

        self.size = 50   #5x5 cells
        self.pos = [5,4]
        self.heading = 'East'

    def proximitySensor(self, environment):
        #checks immediate suroundings for obstacles

        #TODO This assumes a robot size of 5, make it adaptable
        
        pos = self.pos
        
        obsLocations = []


        #check for sides
        for i in range(-2,3,1):
            if environment.map[pos[1]-3][pos[0]+i].value == -1:
                obsLocations.append([pos[0]+i,pos[1]-3])
            if environment.map[pos[1]+3][pos[0]+i].value == -1:
                obsLocations.append([pos[0]+i,pos[1]+3])
            if environment.map[pos[1]+i][pos[0]+3].value == -1:
                obsLocations.append([pos[0]+3,pos[1]+i])
            if environment.map[pos[1]+i][pos[0]-3].value == -1:
                obsLocations.append([pos[0]-3,pos[1]+i])

        #check for corners        
        if environment.map[pos[1]-3][pos[0]-3].value == -1:
            obsLocations.append([pos[0]-3,pos[1]-3])
        if environment.map[pos[1]-3][pos[0]+3].value == -1:
            obsLocations.append([pos[0]+3,pos[1]-3])
        if environment.map[pos[1]+3][pos[0]-3].value == -1:
            obsLocations.append([pos[0]-3,pos[1]+3])
        if environment.map[pos[1]+3][pos[0]+3].value == -1:
            obsLocations.append([pos[0]+3,pos[1]+3])

        return obsLocations
        

    def bumpSensor(self, action, environment):
        b = []
        
        bumpCoordinates = self.getBumpCoordinates(action)

        if bumpCoordinates != None:
            for pos in bumpCoordinates:
                if environment.map[pos[1]][pos[0]].value == -1:
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
            
        

    def dirtSensor(self,environment):
        dValues = []

        #the whole robot is a vacuum!
        for x in range(-2,3,1):
            for y in range (-2,3,1): 
            
                if environment.map[self.pos[1]+x][self.pos[0]+y].value > 0:
                    d = environment.map[self.pos[1]+x][self.pos[0]+y].value
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

        print "robot pos: ",self.pos
        print "robot heading: ",self.heading

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
        return 0

    def generateSuccessor( self, action):
        return 0

    def getRobotPosition( self ):
        return 0
        
    def getDirt( self ):
        return 0

    def getUnvisited( self ):
        return 0

    def getVisited( self ):
        return 0

    def getObstacles( self ):
        return 0

    def __init__ ( self, robot , robotMap ):

        self.r = robot
        self.map = robotMap

if __name__ == "__main__":
    
    #TODO add option to import environment
    #TODO add option for real vs simulated robot

    r = RobotSimulator()
    r.run()
