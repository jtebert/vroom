# Extra functions useful for a variety of things

import heapq


class PriorityQueue:
    """
    Priority Queue data structure based on the Berkeley Pacman Project
    """
    def __init__(self):
        self.heap = []
        self.count = 0

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


class Stack:
    """
    LIFO queue (based on Berkeley Pacman Project
    """
    def __init__(self):
        self.list = []

    def push(self, i):
        self.list.append(i)

    def pop(self):
        return self.list.pop()

    def is_empty(self):
        return len(self.list) == 0


class Grid:

    def __init__(self, grid_size=100):
        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    def __str__(self):
        print_str = ""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                print_str += (str(self.grid[row][col]) + " ")
            print_str += "\n"
        return print_str

    def __repr__(self):
        return str(self)

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
        #print self
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
        Plus 3 in every direction (7x7 grid)
        """
        x, y = pos
        for row in range(x - 3, x + 4):
            if row >= 0 and row < self.grid_size:
                for col in range(y - 3, y + 4):
                    if col >= 0 and col < self.grid_size:
                        self.grid[row][col] = 1

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

    def copy(self):
        g = Grid(self.grid_size)
        g.grid = [x[:] for x in self.grid]
        return g


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
