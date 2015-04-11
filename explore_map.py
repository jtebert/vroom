# Functions to explore and map an unknown environment

import utils


class MapEnvironmentProblem:
    """
    A search problem of visiting (exploring) all squares in an unknown environment
    Updates the robot's knowledge of the environment as it explores

    A search state is a tuple of (RobotState, Grid)
    """

    def __init__(self, start_state, grid_size=100):
        grid = utils.Grid(grid_size)
        grid.visit(start_state.getRobotPosition())
        grid.set_all_valid_actions(start_state)
        self.start = (start_state, grid)

    @staticmethod
    def is_goal_state(state):
        return state[1].are_all_visited()

    @staticmethod
    def get_successors(state):
        """
        Returns successor states (states where you'll explore something new), the actions they require
        :param state: Current robot position & exploration grid
        :return: List of (state, action) tuples
        """
        robot_state = state[0]
        actions = robot_state.getLegalActions()
        successors = []
        for action in actions:
            if state[0].willVisitNewCell(action):
                next_state = robot_state.generateSuccessor(action)
                next_x, next_y = next_state.getRobotPosition()
                # Create new grid with newly visited cells and rechecking whether
                # new cells will be visited
                next_grid = state[1].deepcopy()
                next_grid.mark_visited((next_x, next_y))
                next_grid.set_all_valid_actions(state[0])
                successors.append(((next_state, next_grid), action))
        return successors

    def get_cost_of_actions(self, actions):
        """
        Get cost of a series of actions. Return 999999 if sequence illegal
        :param actions: List of actions
        :return: Numerical cost of actions
        """
        robot_state = self.start[0]
        cost = 0
        for action in actions:
            # Check if legal
            legal = robot_state.getLegalActions()
            if not action in legal:
                return 999999
            robot_state = robot_state.generateSuccessor(action)
            cost += 1
        return cost


def exploration_heuristic(state, problem):
    """
    Heuristic to search all locations in the map
    :param state: Current state of the robot/world
    :param problem: Search problem to be completed (e.g., MapEnvironmentProblem)
    :return: Heuristic value of the current state (RobotState, Grid)
    """
    robot_state, grid = state
    unexplored = grid.list_unexplored()
    cell_costs = []
    for cell in unexplored:
        cell_costs.append(utils.manhattan_distance(robot_state.getRobotPosition(), cell))
    if len(cell_costs) > 0:
        max_cost = max(cell_costs)
    else:
        max_cost = 0
    return max_cost
