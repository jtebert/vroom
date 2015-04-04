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


def manhattan_distance(p1, p2):
    """
    Calculate the Manhattan distance between the 2 points
    :param p1: Tuple (x,y) position
    :param p2: Tuple (x,y) position
    :return: Distance
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])