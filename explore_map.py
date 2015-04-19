# Functions to explore and map an unknown environment

import utils


class MapEnvironmentProblem:
    """
    A search problem of visiting (exploring) all squares in an unknown environment
    Updates the robot's knowledge of the environment as it explores

    A search state is a RobotState
    """

    def __init__(self, start_state):
        self.start = (start_state)

    @staticmethod
    def is_goal_state(state):
        return state.map.are_all_visited()

    @staticmethod
    def get_successors(state):
        """
        Returns the sucessor state that explores the most new cells
        :param state: Current robot position & exploration grid
        :return: List of (state, action) tuples
        """
        actions = state.getLegalActions(state.getRobotPosition())
        #print state.getRobotPosition()
        successor = []
        max_new_cells = 0
        max_new_cells_action = None
        for action in actions:
            n_new_cells = state.willVisitNewCell(state.getRobotPosition(), action)
            if n_new_cells > max_new_cells:
                max_new_cells = n_new_cells
                max_new_cells_action = action

        if max_new_cells_action != None:
            next_state = state.generateSuccessor(max_new_cells_action)
            successor.append((next_state,max_new_cells_action))

        return successor

    def get_cost_of_actions(self, actions):
        """
        Get cost of a series of actions. Return 999999 if sequence illegal
        :param actions: List of actions
        :return: Numerical cost of actions
        """
        cost = 0
        return cost


class GoHomeProblem:
    """
    Problem for the robot to find its way to its home location

    A search state is a RobotState
    """

    def __init__(self, start_state):
        self.start = (start_state)

    @staticmethod
    def is_goal_state(state):
        return state.getRobotPosition() == state.home

    @staticmethod
    def get_successors(state):
        """
        Returns successor states (states where you'll explore something new), the actions they require
        :param state: Current robot position & exploration grid
        :return: List of (state, action) tuples
        """
        actions = state.getLegalActions(state.getRobotPosition())
        #print state.getRobotPosition()
        successors = []
        for action in actions:
                #print action
                next_state = state.generateSuccessor(action)
                successors.append((next_state, action))
        return successors

    def get_cost_of_actions(self, actions):
        """
        Get cost of a series of actions. Return 999999 if sequence illegal
        :param actions: List of actions
        :return: Numerical cost of actions
        """
        robot_state = self.start
        cost = 0
        for action in actions:
            # Check if legal
            legal = robot_state.getLegalActions(robot_state.getRobotPosition())
            if not action in legal:
                return 999999
            robot_state = robot_state.generateSuccessor(action)
            cost += 1
        return cost
