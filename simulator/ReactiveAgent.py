  
from robotState import *



class ReactiveAgent(object):
# Runs a basic reactive agent for an environment


    def __init__(self, maxActions):
        self.actions = []
        self.nActions = 0
        self.maxActions = maxActions
        self.turning = False
        self.initPosition = []
        
    def run (self, state):
        self.initPosition = list([state.r.pos[0],state.r.pos[1]])
        
        while (len(self.actions) < self.maxActions):
            action = None
            bestAction = 0
            #if an action will explore new space, take it
            
            for option in state.getLegalActions(state.r.pos):
                newCells = state.willVisitNewCell(state.r.pos, option)
                if newCells > bestAction:
                    action = option
                    bestAction = newCells

      
            # else take first available action from get legal actions
            # this should result in the robot going north until it hits a wall
            # then follows the wall to the east
            if action == None:
                
                if state.r.pos == self.initPosition:
                    #back at the start...giveup
                    self.maxActions = len(self.actions)
                else:
                    actions = state.getLegalActions(state.r.pos)
                    action = actions[0]

        
            self.actions.append(action)
            state = state.generateSuccessor(action)

        return self.actions
            

        
