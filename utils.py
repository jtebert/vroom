# Extra functions useful for a variety of things

import heapq
import csv
import copy


def reverse_action(action):
    """
    Give the opposite action of that given (go in the opposite direction)
    :param action: North, East, South, West, None
    :return: North, East, South, West, None
    """
    if action == 'North':
        return 'South'
    elif action == 'South':
        return 'North'
    elif action == 'East':
        return 'West'
    elif action == 'West':
        return 'East'
    else:
        return 'None'


class PriorityQueue:
    """
    Priority Queue data structure based on the Berkeley Pacman Project
    """
    def __init__(self):
        self.heap = []
        self.count = 0

    def __str__(self):
        #return str(self.heap)
        return str([str(x[2]) for x in list(self.heap)])

    def push(self, item, priority):
        """
        Add an item with a given priority to the queue
        :param item: Thing to add to the queue
        :param priority: Priority of thing to add
        """
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        """
        Pop the highest priority item from the queue
        """
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        """
        Check if there are no more items in the queue
        """
        return len(self.heap) == 0


class Grid:
    # TODO: Get rid of this (once sure everything is migrated to RobotMap)

    def __init__(self, grid_size=100):
        self.grid_size = grid_size
        self.grid = [[GridCell((y,x)) for y in range(grid_size)] for x in range(grid_size)]

    def __str__(self):
        print_str = ""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                print_str += (str(self.grid[row][col]) + " ")
            print_str += "\n"
        return print_str

    def __repr__(self):
        return str(self)

    def set_all_valid_actions(self, robot_state):
        """
        Use the robot state to determine what actions are valid,
        ONLY for cells that have been visited.
        :param robot_state: RobotState (for the map)
        :return: Nothing. Mutation, man.
        """
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x].is_visited:
                    self.grid[y][x].set_valid_actions(robot_state)

    def is_visited(self, x, y):
        """
        Get whether the grid at position [x][y] has been explored
        :param x: x position
        :param y: y position
        :return: Boolean
        """
        return self.grid[y][x].is_visited

    def are_all_visited(self):
        """
        Check if all explorable cells have been explored.
        If all visited, search mapping is complete
        :return: Boolean, fully explored or not
        """
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x].are_any_valid_actions():
                    return False
        return True

    def visit(self, pos):
        """
        Mark the cell at the pos as explored (1)
        Plus 2 in every direction (5x5 grid)
        """
        g = 2
        x, y = pos
        for row in range(x - g, x + g + 1):
            if row >= 0 and row < self.grid_size:
                for col in range(y - g, y + g + 1):
                    if col >= 0 and col < self.grid_size:
                        self.grid[row][col].visit()

    def copy(self):
        g = Grid(self.grid_size)
        g.grid = [x[:] for x in self.grid]
        return g

    def deepcopy(self):
        g = Grid(self.grid_size)
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                g.grid[x][y] = self.grid[x][y].copy()
        return g


class GridCell(object):
    """
    Represents the current state of the cell (explored, unexplored)
    and list of actions from the cell that will explore new cells
    """

    def __init__(self, coord):
        self.coord = coord
        self.is_visited = False
        self.valid_actions = []

    def __str__(self):
        if self.is_visited:
            return "1"
        else:
            return "0"

    def set_valid_actions(self, robot_state):
        """
        Use the robot state to determine explorative actions from the current cell
        """
        # TODO: Not actually sure if robot_state is updated to have the correct info for checking this?
        new_actions = []
        # TODO: Change this back when getLegalActions is updated
        actions = robot_state.getLegalActions(self.coord)
        #actions = robot_state.getLegalActions()
        for a in actions:
            if robot_state.willVisitNewCell(self.coord, a):
                new_actions.append(a)
        self.valid_actions = new_actions

    def visit(self):
        self.is_visited = True

    def are_any_valid_actions(self):
        return len(self.valid_actions) > 0

    def copy(self):
        gc = GridCell(self.coord)
        gc.is_visited = self.is_visited
        gc.valid_actions = self.valid_actions
        return gc


def manhattan_distance(p1, p2):
    """
    Calculate the Manhattan distance between the 2 points
    :param p1: Tuple (x,y) position
    :param p2: Tuple (x,y) position
    :return: Distance
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def null_heuristic(state, problem=None):
    return 0


def readTrainingMap(fileName):
    csvfile = open(fileName, 'r')
    csvReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    trainingMap = []
    for row in csvReader:
        line = row[0].split(',')
        trainingMap.append(map(int, line))
    return trainingMap


def generateMapOrientations(m):
    orient = list()
    orient.append(copy.deepcopy(m))
    orient.append(rotateMap(orient[0]))
    orient.append(rotateMap(orient[1]))
    orient.append(rotateMap(orient[2]))
    orient.append(flipMap(orient[0]))
    orient.append(flipMap(orient[1]))
    orient.append(flipMap(orient[2]))
    orient.append(flipMap(orient[3]))
    return orient

def rotateMap(m, width = 10, height = 10):
    mcp = copy.deepcopy(m)
    if width != height:
        print "Can't do that"
    else:
        for x in range(0, int(width)):
            for y in range(0, int(height)):
                mcp[y][width - 1 - x] = m[x][y]
        return mcp

def flipMap(m, width = 10, height = 10):
    mcp = copy.deepcopy(m)
    if width != height:
        print "Can't do that"
    else:
        for x in range(0, int(width)):
            for y in range(0, int(height)):
                mcp[x][height - 1 - y] = m[x][y]
        return mcp