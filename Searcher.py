from queue import Queue
from pprint import pprint
import math
from time import sleep
from copy import deepcopy

from BlockHandling import BlockHandler


class Searcher(object):

    def __init__(self, gameField, snake, foodDispatcher):
        self.gameField = gameField
        self.snake = snake
        self.foodDispatcher = foodDispatcher
        self._frontier = Queue()
        #self._all_blocks = all_blocks  # todo: use matrix..?

        x, y = self.gameField.get_game_field_block_size()
        self._blockHandler = BlockHandler(x, y, gameField)
        print(self._blockHandler.get_blocks())

    def _get_relative_point_to_point_distance(self, point1, point2):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def get_relative_head_to_fruit_distance(self):

        # Just tryout
        #pprint(self.gameField.get_game_matrix())

        coo_fruit = self.gameField.map_pixels_to_coordinates(self.foodDispatcher.get_food_position())
        #print pos_fruit
        coo_head = self.gameField.map_pixels_to_coordinates(self.snake.get_head_position())
        #print pos_head
        return self._get_relative_point_to_point_distance(coo_fruit, coo_head)

    def get_relative_point_to_fruit_distance(self, point):
        coo_fruit = self.gameField.map_pixels_to_coordinates(self.foodDispatcher.get_food_position())
        return self._get_relative_point_to_point_distance(coo_fruit, point)

    def get_relative_point_to_head_distance(self, point):
        coo_head = self.gameField.map_pixels_to_coordinates(self.snake.get_head_position())
        return self._get_relative_point_to_point_distance(coo_head, point)

    def test(self):

        snake_positions = self.snake.get_tail_positions()
        head_position = self.snake.get_head_position()
        snake_positions.append(head_position)
        fruit_pos = self.foodDispatcher.get_food_position()
        self._blockHandler.update_blocks(snake_positions, fruit_pos)

        coo_head = self.gameField.map_pixels_to_coordinates(head_position)
        start_element = self._blockHandler.get_block_by_coordinates(coo_head)
        print(start_element)
        self._frontier.put(start_element)
        visited = {}
        visited[start_element.get_id()] = True

        print(self.get_valid_neighbors(self.get_neighbor_coordinates(start_element)))

    def scan(self):

        pos_head = self.gameField.map_pixels_to_coordinates(self.snake.get_head_position())

        start_element = self._blockHandler.get_block_by_coordinates(self.gameField.map_pixels_to_coordinates(pos_head))
        print(start_element)
        self._frontier.put(start_element)

        visited = {}
        visited[start_element] = True

        while not self._frontier.empty():
            current = self._frontier.get()
            for next in self.get_valid_neighbors(self.get_neighbor_coordinates(current)):
                self._frontier.put(next)
                visited[next] = True
                # todo

    def get_neighbor_coordinates(self, block):

        neighbors_coordinates = []
        c_x, c_y = block.get_coordinates()
        print("Block coordinates: %s %s" % (c_x, c_y))

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

    def get_valid_neighbors(self, neighbor_coordinates):
        """

        Returns list of valid coordinates

        :param neighbor_coordinates:
        :return:
        """
        valid_blocks = []

        #game_matrix = self.gameField.get_game_matrix()
        #print(pprint(game_matrix))
        for c in neighbor_coordinates:
            #if game_matrix[c[1]][c[0]] == 1:  # Tail, Beware: Matrix access first Y-axis, then X-axis!
            #    continue
            #if game_matrix[c[1]][c[0]] == 2:  # Head, Beware: Matrix access first Y-axis, then X-axis!
            #    continue
            for b in self._blockHandler.get_blocks():
                if b.get_block_type() == "tail":
                    continue
                elif b.get_block_type() == "head":
                    continue
                if b.get_coordinates() == c:
                    print("Match: %s (%s)" % (b, c))
                    valid_blocks.append(b)
        return valid_blocks
