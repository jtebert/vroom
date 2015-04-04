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
