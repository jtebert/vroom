
from simulator.map import *


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


        while(True):
            self.listenControls()
            screen = pygame.display.get_surface()

            if self.action != None:
                #check bumper 
                bumpReadings = self.robot.bumpSensor(self.action,self.environment)
                dirtReading = self.robot.dirtSensor(self.environment)

                if (dirtReading > 0):
                    print "maping dirt value: ",dirtReading
                    self.map.map[self.robot.pos[1]][self.robot.pos[0]].dirt = dirtReading

                if(not(self.robot.isBump(bumpReadings))):
                    self.robot.takeAction(self.action)
                else:
                    for reading in bumpReadings:
                        self.map.map[reading[1]][reading[0]].isObstacle = True
                    
                self.action = None

            screen.fill((204,204,204))  
            
            if self.showEnvironment:
                self.map.draw(screen,environment = self.environment)
                self.map.drawRobot
            else:
                self.map.draw(screen)
                self.map.drawRobot(screen,self.robot)
            

            
            pygame.display.update()


        

class Robot(object):

    def __init__(self,environment):

        self.size = 50   #5x5 cells
        self.pos = [10,10]
        self.heading = 'North'

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
                          [self.pos[0]-2,self.pos[1]-2],
                          [self.pos[0]+2,self.pos[1]-2]]

            if action == 'South':
                coords = [[self.pos[0]+1,self.pos[1]+3],
                          [self.pos[0],self.pos[1]+3], 
                          [self.pos[0]-1,self.pos[1]+3],
                          [self.pos[0]-2,self.pos[1]+2],
                          [self.pos[0]+2,self.pos[1]+2]]

            if action == 'East':
                coords = [[self.pos[0]+3,self.pos[1]], 
                          [self.pos[0]+3,self.pos[1]-1],
                          [self.pos[0]+3,self.pos[1]+1],
                          [self.pos[0]+2,self.pos[1]-2],
                          [self.pos[0]+2,self.pos[1]+2]]

            if action == 'West':
                coords = [[self.pos[0]-3,self.pos[1]], 
                          [self.pos[0]-3,self.pos[1]-1],
                          [self.pos[0]-3,self.pos[1]+1]]

        return coords
            


    def dirtSensor(self,environment):
        d = -1

        if environment.map[self.pos[1]][self.pos[0]].value > 0:
            d = environment.map[self.pos[1]][self.pos[0]].value
            
            print "found dirt : ",d
        
        return d


    def takeAction(self,action):
        
        if self.heading == action:
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
            if action == 'East':
                heading = 'East'
            if action == 'West':
                heading = 'West'

        if self.heading == 'East':
            if action == 'South':
                heading = 'South'
            if action == 'North':
                heading = 'North'

        if self.heading == 'South':
            if action == 'West':
                heading = 'West'
            if action == 'East':
                heading = 'East'
                
        if self.heading == 'West':
            if action == 'North':
                heading = 'North'
            if action == 'South':
                heading = 'South'

        return heading


if __name__ == "__main__":
    
    #TODO add option to import environment
    #TODO add option for real vs simulated robot

    r = RobotSimulator()
    r.run()
