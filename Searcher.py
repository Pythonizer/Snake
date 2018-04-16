from Queue import Queue
from pprint import pprint
import math
from time import sleep
from copy import deepcopy


class Searcher(object):

    def __init__(self, gameField, snake, foodDispatcher):
        self.gameField = gameField
        self.snake = snake
        self.foodDispatcher = foodDispatcher
        self._frontier = Queue()
        #self._all_blocks = all_blocks  # todo: use matrix..?

    def _get_relative_point_to_point_distance(self, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def get_relative_head_to_fruit_distance(self):

        # Just tryout
        pprint(self.gameField.get_game_matrix())

        pos_fruit = self.gameField.map_pixels_to_coordinates(self.foodDispatcher.get_food_position())
        print pos_fruit
        pos_head = self.gameField.map_pixels_to_coordinates(self.snake.get_head_position())
        print pos_head
        return self._get_relative_point_to_point_distance(pos_fruit, pos_head)

    def get_relative_point_to_fruit_distance(self, point):
        pos_fruit = self.gameField.map_pixels_to_coordinates(self.foodDispatcher.get_food_position())
        return self._get_relative_point_to_point_distance(pos_fruit, point)

    def get_relative_point_to_head_distance(self, point):
        pos_head = self.gameField.map_pixels_to_coordinates(self.snake.get_head_position())
        return self._get_relative_point_to_point_distance(pos_head, point)

    def scan(self):
        pass
        pos_head = self.gameField.map_pixels_to_coordinates(self.snake.get_head_position())
        start_element = deepcopy(pos_head)
        self._frontier.put(start_element)

        visited = {}
        visited[start_element] = True
        tmp_marker = 1

        while not self._frontier.empty():
            current = self._frontier.get()
            for next in self.get_neighbors(current):
                self._frontier.put(next)
                visited[next] = True
                # todo


        # Put start element in queue
        # create visited-dict
        # put start element (coordinates?) as key in dict and set visited to true
        # set tmp_marker... why?^^
        # while queue not empty
        #  current = queue.get()
        #  for next in neighbors of current
        #   put next in queue
        #   put next in visited-dict and set to true

    def get_neighbors(self, pos):
        return self.get_valid_neighbors(pos)

    def get_neighbor_coordinates(self, block):

        neighbors_coordinates = []
        c_x, c_y = block.get_coordinates()
        print "Block coordinates: %s %s" % (c_x, c_y)

        # (+1, 0)
        if c_x + 1 <= 5:
            neighbors_coordinates.append((c_x+1, c_y))
        # (-1, 0)
        if c_x - 1 >= 0:
            neighbors_coordinates.append((c_x - 1, c_y))
        # (0, +1)
        if c_y + 1 <= 5:
            neighbors_coordinates.append((c_x, c_y + 1))
        # (0, -1)
        if c_y - 1 >= 0:
            neighbors_coordinates.append((c_x, c_y - 1))

        return neighbors_coordinates

    def get_valid_neighbors(self, n_coordinates):
        valid_blocks = []
        for c in n_coordinates:
            #print c
            for b in self._all_blocks:
                if b.get_block_type() == "barrier":  # todo: check if != 1 or 2
                    continue
                if b.get_coordinates() == c:
                    print "Match: %s (%s)" % (b, c)
                    valid_blocks.append(b)
        return valid_blocks
