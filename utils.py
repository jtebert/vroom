# Extra functions useful for a variety of things


class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    NONE = 'None'


def manhattan_distance(p1, p2):
    """
    Calculate the Manhattan distance between the 2 points
    :param p1: Tuple (x,y) position
    :param p2: Tuple (x,y) position
    :return: Distance
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])