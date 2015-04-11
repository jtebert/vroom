# Functions to explore and map an unknown environment

import utils


# TODO: Check if there are unreachable position? (eliminate from search)


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
                successors.append(( (next_state, next_grid), action))
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


class Node:
    """
    This class contains a state, cost to reach that state (from parent or general?), last action, and reference to
    parent Node
    """

    def __init__(self, state, prev_action, parent, problem, heuristic=utils.null_heuristic):
        self.state = state
        self.prev_action = prev_action
        self.parent = parent
        self.heuristic = heuristic
        self.cost = self.get_cost_estimate(problem)

    def __str__(self):
        return str(self.state)

    def has_parent(self):
        """
        Check if parent node is None
        """
        return self.parent is not None

    def get_path_reversed(self):
        """
        Get the path to this Node (directions) based on parent Nodes, until no more parents (Batman!)
        Comes out in the wrong order for Pacman so needs to be reversed
        """
        path = []
        if self.has_parent():
            path.append(self.prev_action)
            path.extend(self.parent.get_path_reversed())
        return path

    def get_path(self):
        """
        Reverse the result of getPathReversed to make Pacman happy
        """
        path = self.get_path_reversed()
        path.reverse()
        return path

    def get_path_cost(self, problem):
        """
        Get the cost from the starting position to the current Node
        """
        path = self.get_path()
        return problem.get_cost_of_actions(path)

    def get_cost_estimate(self, problem):
        """
        Get the estimated cost based on cost (from start) and heuristic (estimate to goal)
        """
        path_cost = self.get_path_cost(problem)
        heuristic_cost = self.heuristic(self.state, problem)
        return path_cost + heuristic_cost


#TODO: This is not relevant for mapping anymore. Hang onto for dirt search later
def a_star_search(problem, heuristic):
    """
    Search the problem with the heuristic to find lowest cost option
    :param problem: Problem, e.g. MapEnvironmentProblem
    :param heuristic: e.g. exploration_heuristic
    :return: Actions to take
    """
    n0 = Node(problem.start, None, None, problem, heuristic)
    if problem.is_goal_state(n0.state):
        return ['None']
    frontier = utils.PriorityQueue()
    frontier.push(n0, n0.cost)
    explored = set()
    while not frontier.is_empty():
        node = frontier.pop()
        explored.add(node.state)
        if problem.is_goal_state(node.state):
            return node.getPath()
        next_states = problem.get_successors(node.state)
        frontier_costs = []
        frontier_states = []
        for n in frontier.heap:
            frontier_states.append(n[2].state)
            frontier_costs.append(n[2].cost)
        for next_state in next_states:
    
            next_node = Node(next_state[0], next_state[1], node, problem, heuristic)
            if (next_node.state not in explored and next_node.state not in frontier_states) or \
                    (next_node.state in frontier_states and frontier_costs[
                        frontier_states.index(next_node.state)] > next_node.cost):
                frontier.push(next_node, next_node.cost)
    return ["None"]


# Let's try this again...
# Depth first search, with backtracking, minimizing revisiting of visited nodes
# End when all explored or nothing else reachable (will backtrack to starting position and have nowhere else to go)
def depth_first_search(problem):
    """
    Depth first search, with backtracking, minimizing revisiting of visited nodes
    End when all explored or nothing else reachable (will backtrack to starting position and have nowhere else to go)
    :param problem:
    :return: Path of actions (list)
    """
    node = Node(problem.start, None, None, problem)
    while not problem.is_goal_state(node.state):
        next_states = problem.get_successors(node.state)
        if len(next_states) == 0:
            # Nothing new to explore from current location; backtrack
            next_state = node.parent.state
        else:
            next_state = next_states[0]
        node = Node(next_state[0], next_state[2], node, problem)
    return node.get_path()

# Run the search:
#problem = MapEnvironmentProblem(robot_start_state)
#a_star_search(problem, exploration_heuristic)
