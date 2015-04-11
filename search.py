import utils


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