import utils


class CollectDirtProblem(object):
    """
    A search problem of collecting all dirt in the environment
    A search state is the RobotState
    """

    def __init__(self, start_state):
        self.start = start_state

    @staticmethod
    def is_goal_state(state):
        """
        Has all the dirt been collected?
        :param state: Current state of the robot
        :return: Boolean (cleaned or not)
        """
        return len(state.getDirt()) == 0

    @staticmethod
    def get_successors(state):
        """
        Returns successor states of legal actions
        :param state: Current robot state
        :return: List of (state, action) tuples
        """
        actions = state.getLegalActions(state.getRobotPosition())
        successors = []
        for action in actions:
            if state.willVisitNewCell(state.getRobotPosition(), action):
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
            legal = robot_state.getLegalActions()
            if not action in legal:
                return 999999
            robot_state = robot_state.generateSuccessor(action)
            cost += 1
        return cost


def dirt_heuristic(state, problem):
    """
    Heuristic to search all locations in the map
    Uses distance to furthest dirt as heuristic
    :param state: Current state of the robot/world (RobotState)
    :param problem: Search problem to be completed (e.g., MapEnvironmentProblem)
    :return: Heuristic value of the current state (RobotState, Grid)
    """
    unvisited = state.map.unvisitedCells
    cell_costs = []
    for cell in unvisited:
        cell_costs.append(utils.manhattan_distance(state.getRobotPosition(), cell))
    if len(cell_costs) > 0:
        max_cost = max(cell_costs)
    else:
        max_cost = 0
    return max_cost
