import utils

# Functions to explore and map an unknown environment


# Maximum estimated grid size?
# Check if there are unreachable position? (eliminate from search)


class Grid:

    def __init__(self, grid_size=100):
        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    def pos(self, x, y):
        """
        Get the value of the grid at position [x][y]
        :param x: x position
        :param y: y position
        :return: -1, 0, 1
        """
        return self.grid[x][y]

    def are_all_explored(self):
        """
        Check if all explorable cells have been explored (no 0s)
        :return: Boolean, fully explored or not)
        """
        return all([all(x) for x in self.grid])

    def mark_unreachable(self, pos):
        """
        Mark the cell at the pos as unreachable (-1)
        """
        x, y = pos
        self.grid[x][y] = -1

    def mark_explored(self, pos):
        """
        Mark the cell at the pos as explored (1)
        """
        x, y = pos
        self.grid[x][y] = 1

    def list_unexplored(self):
        """
        Create a list of all unexplored cells in the grid
        """
        unexp = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] == 0:
                    unexp.append((x, y))
        return unexp


class MapEnvironmentProblem:
    """
    A search problem of visiting (exploring) all squares in an unknown environment
    Updates the robot's knowledge of the environment as it explores

    A search state is a tuple of (RobotState, Grid)
    """

    def __init__(self, start_state):
        init_grid_size = 50
        init_grid = [[0 for _ in range(init_grid_size)] for _ in range(init_grid_size)]
        self.start = (start_state, init_grid)

    def is_goal_state(self, state):
        return state[1].are_all_explored()

    def get_successors(self, state):
        """
        Returns successor states, the actions they require
        :param state: Current robot position & exploration grid
        :return: List of (state, action) tuples
        """
        robot_state = state[0]
        actions = robot_state.getLegalActions()
        successors = []
        for action in actions:
            next_state = robot_state.getSuccessor(action)
            next_x, next_y = next_state.getRobotPosition()
            next_grid = state[1].copy()
            # Mark next cell as explored
            next_grid.mark_explored((next_x, next_y))
            successors.append((next_state, action))
        return successors

    def get_cost_of_actions(self, actions):
        """
        Get cost of a series of actions. Return 999999 if sequence illegal
        :param actions: List of actions
        :return: Numerical cost of actions
        """
        state = self.start[0]
        cost = 0
        for action in actions:
            # Check if legal
            legal = state.getLegalActions()
            if not action in legal:
                return 999999
            state = state.getSuccessor(action)
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


"""
class ExplorationSearchAgent:
    "Agent to explore the map with A* search"
    def __init__(self):
        self.search_function = lambda prob: search.AStarSearch(prob, exploration_heuristic)
        self.search_type = MapEnvironmentProblem
"""


