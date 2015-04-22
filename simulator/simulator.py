from map import *

import os,sys,inspect, getopt
import cPickle as pickle


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 
from explore_map import *
from dirt_collection import *
from search import *
from classifiers import *
from evaluation import *
from robotState import *
from robot import *
from ReactiveAgent import *

import time

class RobotSimulator(object):

    def __init__(self, inputEnv):
            
        
        # the world
        self.environment = Environment(environmentCSV=inputEnv)
        self.envName = inputEnv

        # what the robot knows
        self.map = RobotMap()

        # the robot needs the environment so the sensors can reference it for readings
        self.robot = Robot(self.environment)

        self.showEnvironment = False
        self.k = None
        self.action = None

        self.start = False
        self.updateDirt = False
        self.drawLabels = False

        self.classifiers = Classifiers()
        
    
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
                if self.k == pygame.K_l:
                    self.drawLabels = (not self.drawLabels)
            

    @staticmethod
    def executeDirtSearch (state):
        startTime = time.clock()
        problem = CollectDirtProblem(state)
        actions = a_star_search(problem, dirt_heuristic)
        endTime = time.clock()
        print "a_star_search executed in %d seconds!"%(endTime - startTime)
        return actions

    @staticmethod
    def performEvaluation(state):
        
        # Calculate and plot classification accuracy
        actual, classified, labels = classification_accuracy(state.map, state.r.environment)
        plot_classification_accuracy(actual, classified, labels)

        # Calculate and plot different dirt collection for different methods
        time_steps, collected = all_dirt_collection_rates(state, state.r.environment)
        plot_dirt_collection_rates(time_steps, collected)
    
    @staticmethod
    def executeFeatureExtraction (state, classifiers):
        #print "COUNTS"
        #print utils.countLabels(state.r.environment.map)
        state.featureExtraction(state.map, classifiers)
        #print utils.countLabels(state.r.environment.map)

    @staticmethod
    def executeExploration (state):
        initState = state.copy()
        startTime = time.clock()
        problem = MapEnvironmentProblem(state)
        state = depth_first_search(problem)
        endTime = time.clock()
        print "exploration executed in %d seconds!"%(endTime - startTime)
        return state


    def run(self, simulatorArgs):

        actions = None

        # Set valid actions for the robot's starting position
        # (otherwise no actions to begin with and it stops)
        state = RobotState(self.robot,self.map )
        pos = state.getRobotPosition()
        state.map.map[pos[0]][pos[1]].set_valid_actions(state)

    
        if simulatorArgs["exploreSearch"]:

            if simulatorArgs ["usePickle"]:
                pickleName = self.getPickleName("explore")
                if os.path.isfile(pickleName):
                    print "explore pickle available for %s "%(self.envName)
                    print "skipping exploration phase...."
                    state = pickle.load( open( pickleName, "rb"))
                else:
                    state = self.executeExploration(state)
                    pickle.dump(state, open( pickleName, "wb"))

            else:
                state = self.executeExploration(state)
                pickleName = self.getPickleName("explore")
                pickle.dump(state, open( pickleName, "wb"))
                    
        elif simulatorArgs["reactiveAgent"]:
            agent = ReactiveAgent(1000)
            actions = agent.run(state)
            print actions
        else:
            #like we have explored the map
            if not simulatorArgs["joyStickMode"]:
                state.map = self.environment.copyEnvIntoMap(state.map)

        # DIRT COLLECTION PROBLEM
        # This needs to run if we do not explore the environment
        #state.map = self.environment.copyEnvIntoMap(state.map)

        if simulatorArgs["runClassification"] == True:
            self.executeFeatureExtraction(state, self.classifiers)

        # update environments dirt
        # invoke multiple times?
        state.r.environment.updateDirt()
        
        # clear robots dirt after feature extraction
        state.clearDirt()
        
        afterDirtUpdateState = state.copy()

        # update robots prediction of dirt
        print "before updating dirt predictons: ",state.getDirt()
        state.map.updateDirt()
        state.updateDirtList()
        state.removeUnreachableDirt()
        #print "after updating dirt predictions: ",state.getDirt()

        #only needed if we explore then search
        if simulatorArgs["exploreSearch"] == True:
            state = state.resetMission()

        if simulatorArgs["runEvaluation"] == True:
            try: 
                self.performEvaluation(state)
            except ImportError,e:
                print "module not found: %s"%(e)
                print "SKIPPING EVALUATION PHASE!"
                pass
            except Exception ,e:
                print "Error running evaluation: %s"%(e)
                pass
            

        if simulatorArgs["exploreSearch"]:
            actions = self.executeDirtSearch(state)        
            state = afterDirtUpdateState


        pygame.init()
        pygame.display.set_mode((700,700), pygame.RESIZABLE)
        pygame.display.update()

        while(True):

            
            if (actions == None):
                self.listenControls()

                if self.updateDirt:
                    self.updateDirt = False
                    self.environment.updateDirt()
                #self.action is set directly by self.listenControls
            else:
                if len(actions):
                    self.action = actions.pop(0)
                else:
                    self.action = 'None'
                time.sleep(0.1)
            
            screen = pygame.display.get_surface()
            state = state.generateSuccessor(self.action)

            #update Screen
            screen.fill((204,204,204))
            if self.showEnvironment:
                state.map.draw(screen,environment = state.r.environment)
            else:
                state.map.draw(screen)
            state.map.drawRobot(screen,state.r)
            if self.drawLabels:
                state.map.drawLabels(screen)
            pygame.display.update()

            #print state.r.pos


    def getPickleName (self, action):
        #pickles file name will be 
        #action_envName.p

        env = self.extractEnvName()
        pickleName = str(action) + '_' + str(env) + '.p'

        return pickleName

    def extractEnvName (self):
        #This will break if we move the assets folder...

        envName = str(self.envName)
        #envs are in ..\assets\maps\"envname"  
        #so split 3 \'s and .csv to get envname
        
        index = envName.find('/')
        envName = envName[(index+1):]
        
        index = envName.find('/')
        envName = envName[(index+1):]
        
        index = envName.find('/')
        envName = envName[(index+1):]

        index = envName.find('.')
        envName = envName[:index]

        print envName        

        return envName

def printBanner():
    print("")
    print("")
    print("====================================================================================================")
    print("           '   +++      ++;:++++++++;   '+++++++   :+++++++:  ++       ++' ++                       ")
    print(" ;+++++++++++  +++     +++ ++++++++++  ++++++++++ ++++++++++  +++     +++  ++       ++++++++++++'   ")
    print("           ;'   ++    :++         +++  ++     +++ ++;     ++ :+++    '+++ ;++    ++++++++++++++++++ ")
    print("                ++;   ++          +++ '++     +++ ++      ++ +++++   ++++ +++   ++++++++++++++++++++")
    print("     ;'+++++++  +++  +++   +++++++++' +++     ++  ++     '++ +++++  +++++ ++:  +++++++++++++++++++++")
    print("        ,;'+++   ++ +++    +++++++++  ++:     ++ ;++     +++ ++ ++;++++++ ++   +++++++++++++++     '")
    print("                 ++;++    +++  +++    ++      ++ +++     ++  ++ +++++ ++       ++++++++++++++++     ")
    print("         ;'++++  ++++'    +++   +++   ++++++++++ ++++++++++ :++ ;+++  ++ ;++   +++++++++++++++++    ")
    print("      :'+++++++   +++     ++    ;+++  +++++++++  ++++++++++ +++  ++   ++ +++     +++       +++      ")
    print("====================================================================================================")
    print("")
    print("")

def printHelp():
    print "VROOM Simulator: available options"
    print "Default to joystick mode. Use arrow keys to explore environment"
    print "-e <environmentpath> : sets the environment the robot will explore"
    print "-a : run all options: explore -> classify -> evaluation functions"
    print "-v : run evaluation functions"
    print "-f : run classification " 
    print "-s : run exploration then search function"
    print "-r : run the reactive agent"
    print "-p : use pickle files if available"   
    print ""

if __name__ == "__main__":
    
    
    try: 
        opts,args = getopt.getopt(sys.argv[1:],"pavshfire:")
    except getopt.GetoptError:
        printBanner()
        printHelp()
        sys.exit(2)
        

    #defaultEnvironmentCSV = './../assets/maps/basement.csv'
    defaultEnvironmentCSV = './../assets/maps/roomwithcloset1.csv'
    saveMapEnvAtEnd = False

    simulatorArgs = { "runEvaluation" : False,
                      "joyStickMode" : True,
                      "exploreSearch" : False,
                      "runClassification" : False,
                      "reactiveAgent"  : False,
                      "usePickle"      : False }

    for opt,arg in opts:
        if opt == '-h':
            printBanner()
            printHelp()
            sys.exit(0)
            
        if opt == '-e':
            defaultEnvironmentCSV = arg
        if opt == '-i':
            saveMapEnvAtEnd = True
        if opt == '-v':
            simulatorArgs["runEvaluation"] = True
            simulatorArgs["joyStickMode"] = False
        if opt == '-a':
            simulatorArgs["runEvaluation"] = True
            simulatorArgs["runClassification"] = True
            simulatorArgs["exploreSearch"] = True
            simulatorArgs["joyStickMode"] = False
        if opt == '-f':
            simulatorArgs["runClassification"] = True
            simulatorArgs["joyStickMode"] = False
        if opt == '-s':
            simulatorArgs["exploreSearch"] = True
            simulatorArgs["joyStickMode"] = False
        if opt == '-r':
            simulatorArgs["reactiveAgent"] = True
            simulatorArgs["joyStickMode"] = False
        if opt == '-p':
            simulatorArgs["usePickle"] = True


    r = RobotSimulator(defaultEnvironmentCSV)

    if saveMapEnvAtEnd:
        try:
            r.run(simulatorArgs)
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
        r.run(simulatorArgs)




