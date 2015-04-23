
        
class Robot(object):

    def __init__(self,environment, pos=[5,7],heading='East'):

        self.size = 50   #5x5 cells
        self.pos = pos
        self.heading = heading
        self.environment = environment
        self.home = pos

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


    def bumpSensor(self, action, position = None):
        b = []

        if position == None:
            pos = self.pos
        else:
            pos = position

        bumpCoordinates = self.getBumpCoordinates(action, pos)

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

    def getBumpCoordinates(self, action, position):

        coords = []
        pos = position

        if action == 'North':
            y = -3
            for i in range(-2,3,1):
                coords.append([pos[0]+i,pos[1]+y])

        if action == 'South':
            y = 3
            for i in range(-2,3,1):
                coords.append([pos[0]+i,pos[1]+y])

        if action == 'East':
            x = 3
            for i in range(-2,3,1):
                coords.append([pos[0]+x,pos[1]+i])

        if action == 'West':
            x = -3
            for i in range(-2,3,1):
                coords.append([pos[0]+x,pos[1]+i])

        return coords



    def dirtSensor(self):
        dValues = []

        #the whole robot is a vacuum!
        for x in range(-2,3,1):
            for y in range (-2,3,1):

                if self.environment.map[self.pos[0]+x][self.pos[1]+y].dirt > 0:
                    d = self.environment.map[self.pos[0]+x][self.pos[1]+y].dirt
                    dValues.append([self.pos[0]+x,self.pos[1]+y,d])

        return dValues


    def takeAction(self,action):

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

        if (action != 'None'):
            self.heading = action


    def evaluateTurn(self,action):
        #not needed anymore

        raise Exception("evaluateTurn is not supported by simulator")


    def copy(self, copyEnv = False):
        if copyEnv:
            environment = self.environment.copy()
        else:
            environment = self.environment
        r = Robot(environment)
        r.pos = list(self.pos)
        r.heading = self.heading
        return r


