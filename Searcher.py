from queue import Queue
from pprint import pprint
from math import sqrt
from time import sleep
from copy import deepcopy


class Searcher(object):

    def __init__(self, gameField, snake, foodDispatcher):
        self.gameField = gameField
        self.snake = snake
        self.foodDispatcher = foodDispatcher
        self._frontier = Queue()

    def get_heuristic_food_distance(self, node):
        point1 = node.get_coordinates()
        point2 = self.foodDispatcher.get_food_coordinates()
        dx = abs(point1[0] - point2[0])
        dy = abs(point1[1] - point2[1])
        #return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
        round(10 * sqrt(dx ** 2 + dy ** 2))
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def get_neighbors(self, node, nodes):
        return self._get_valid_neighbors(self._get_neighbor_coordinates(node), nodes)

    def _get_neighbor_coordinates(self, block):

        neighbors_coordinates = []
        c_x, c_y = block.get_coordinates()
        #print("Block coordinates: %s %s" % (c_x, c_y))

        # (+1, 0)
        if c_x + 1 <= 19:
            neighbors_coordinates.append((c_x+1, c_y))
        # (-1, 0)
        if c_x - 1 >= 0:
            neighbors_coordinates.append((c_x - 1, c_y))
        # (0, +1)
        if c_y + 1 <= 19:
            neighbors_coordinates.append((c_x, c_y + 1))
        # (0, -1)
        if c_y - 1 >= 0:
            neighbors_coordinates.append((c_x, c_y - 1))

        return neighbors_coordinates

    def _get_valid_neighbors(self, neighbor_coordinates, nodes):
        """

        Returns list of valid coordinates

        :param neighbor_coordinates:
        :return:
        """
        valid_blocks = []

        for c in neighbor_coordinates:
            for n in nodes:
                if n.get_node_type() == "blocking_node":
                    continue
                elif n.get_node_type() == "start_node":
                    continue
                if n.get_coordinates() == c:
                    #print("Match: %s (%s)" % (n, c))
                    valid_blocks.append(n)
        return valid_blocks
