
from Settings import BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE

from Searcher import Searcher

from Node import Node

from copy import deepcopy, copy

from pprint import pprint

import pygame


class AI(object):
    def __init__(self, snake, food_dispatcher, gameField):
        self._snake = snake
        self._foodDispatcher = food_dispatcher
        self._gameField = gameField
        self._last_move_direction = None

        self.searcher = Searcher(gameField, snake, food_dispatcher)

        self._path = None
        self._path_back_exists = None
        self._path_to_tail = None
        self._start_node = None
        self._target_node = None
        self._nodes = None

    def _get_path_back_existance(self):
        """

        self._snake.get_tail_positions() (example)
            (410.0, 380.0)  # Last tail-part at position 0
            (380.0, 380.0)
            (350.0, 380.0)
            (320.0, 380.0)
            (290.0, 380.0)
            (260.0, 380.0)
            (230.0, 380.0)
            # Next would be head

        self._path (example)
            [Node(coordinate_x=10, coordinate_y=9, node_type='free',
            Node(coordinate_x=10, coordinate_y=8, node_type='free',
            Node(coordinate_x=10, coordinate_y=7, node_type='free',
            Node(coordinate_x=10, coordinate_y=6, node_type='free',
            Node(coordinate_x=11, coordinate_y=6, node_type='free',
            Node(coordinate_x=12, coordinate_y=6, node_type='free',
            Node(coordinate_x=13, coordinate_y=6, node_type='free',
            Node(coordinate_x=14, coordinate_y=6, node_type='free',
            Node(coordinate_x=15, coordinate_y=6, node_type='free',
            Node(coordinate_x=16, coordinate_y=6, node_type='free',
            Node(coordinate_x=17, coordinate_y=6, node_type='free',
            Node(coordinate_x=18, coordinate_y=6, node_type='target_node']

        :return:
        """

        virtual_nodes = []

        # Get a list of the snakes coordinates (tail & head)
        real_tail_positions = self._snake.get_tail_positions()
        real_tail_coordinates = list(map(lambda real_pos: self._gameField.map_pixels_to_coordinates(real_pos), real_tail_positions))
        real_snake_coordinates = real_tail_coordinates
        real_snake_coordinates.append(self._gameField.map_pixels_to_coordinates(self._snake.get_head_position()))

        # Make a copy of the planed path
        virtual_path = deepcopy(self._path)

        # The virtual start node will be the last piece of the path
        virtual_start_node = copy(virtual_path[-1])
        virtual_start_node.set_node_type('start_node')

        # Find out virtual target. The +/- 1 is for the head
        # Beware that one tail will appear after eat!
        virtual_blocking_coordinates = []
        if len(real_snake_coordinates) > len(virtual_path):
            # Set virtual target node
            v_target_index = len(virtual_path) - 1
            v_target_coo = real_snake_coordinates[v_target_index]
            virtual_target_node = Node(v_target_coo[0], v_target_coo[1], node_type="target_node")

            # Virtual moved snake will be free, except the virtual_target

            # Make remaining snake blocking, except the virtual_target
            start_of_blocking_snake = len(virtual_path)
            for i in range(start_of_blocking_snake, len(real_snake_coordinates)):
                virtual_blocking_coordinates.append(real_snake_coordinates[i])

            # Remove last node of path because its the real target/ virtual_start_node
            if virtual_path:
                virtual_path.pop(-1)

            # The rest of the path is blocking
            for vp_node in virtual_path:
                virtual_blocking_coordinates.append(vp_node.get_coordinates())

        elif len(real_snake_coordinates) < len(virtual_path):
            # Reverse virtual path
            virtual_path_reversed = virtual_path[::-1]

            v_target_index = len(real_snake_coordinates)  # + 1
            # Get virtual target
            virtual_target_node = virtual_path_reversed.pop(v_target_index)
            virtual_target_node.set_node_type("target_node")

            # Last bit of virtual path (length of snake) will be blocking
            for i in range(1, len(real_snake_coordinates)):
                virtual_blocking_coordinates.append(virtual_path_reversed[i].get_coordinates())
            # Whole snake will be free

        else:
            # Path, except last node, is blocking
            for i in range(0, len(virtual_path)-1):
                virtual_blocking_coordinates.append(virtual_path[i].get_coordinates())

            # Virtual target
            virtual_target_coordinates = real_snake_coordinates.pop(-1)
            virtual_target_node = Node(virtual_target_coordinates[0], virtual_target_coordinates[1], 'target_node')
            # Remaining snake will be free

        playground = self._gameField.get_play_ground_positions()
        coordinate_playground = list(map(lambda c: self._gameField.map_pixels_to_coordinates(c), playground))
        for coordinates in coordinate_playground:

            if coordinates in virtual_blocking_coordinates:
                virtual_nodes.append(Node(coordinates[0], coordinates[1], node_type="blocking_node"))

            elif coordinates == virtual_start_node.get_coordinates():
                virtual_nodes.append(virtual_start_node)

            elif coordinates == virtual_target_node.get_coordinates():
                virtual_nodes.append(virtual_target_node)
            else:
                virtual_nodes.append(Node(coordinates[0], coordinates[1]))

        virtual_path_back = self._get_path(virtual_start_node, virtual_target_node, virtual_nodes)

        # Used to assert node results
        if False:
            if not len(virtual_nodes) == 400:
                raise RuntimeError("len(virtual_nodes != 400, %s" % len(virtual_nodes))
            c_s = 0
            c_t = 0
            c_b = 0
            for n in virtual_nodes:
                if n.get_node_type() == 'target_node':
                    c_t += 1
                elif n.get_node_type() == 'start_node':
                    c_s += 1
                elif n.get_node_type() == 'blocking_node':
                    c_b += 1
            if c_s != 1:
                print(virtual_start_node)
                print(virtual_target_node)
                pprint(virtual_nodes)
                raise RuntimeError("VStart node != 1, %s" % c_s)
            if c_t != 1:
                raise RuntimeError("VTarget node != 1, %s" % c_t)
            if c_b != len(virtual_blocking_coordinates):
                pprint(virtual_blocking_coordinates)
                pprint(virtual_nodes)
                raise RuntimeError("Blocking nodes %s != %s" % (len(virtual_blocking_coordinates), c_b))

            print('\n')
            print('VStart: %s' % virtual_start_node)
            print('VTarget: %s' % virtual_target_node)
            print('VBlocking:')
            pprint(virtual_blocking_coordinates)

        return True if virtual_path_back else False

    def _get_path_to_tail(self):
        playground_coordinates = self._gameField.get_playground_coordinates()
        head_coordinate = self._gameField.map_pixels_to_coordinates(self._snake.get_head_position())
        tail_coordinates = list(map(lambda pos: self._gameField.map_pixels_to_coordinates(pos), self._snake.get_tail_positions()))
        print("Tail-Coordinates: %s" % tail_coordinates)
        last_tail_coordinate = tail_coordinates.pop(0)
        print('Head: %s' % str(head_coordinate))
        print("Target_tail: %s" % str(last_tail_coordinate))

        self._start_node = None
        target_tail_node = None
        path_to_tail_nodes = []

        for coordinates in playground_coordinates:
            if coordinates == head_coordinate:
                self._start_node = Node(coordinates[0], coordinates[1], node_type="start_node")
                path_to_tail_nodes.append(self._start_node)
            elif coordinates in tail_coordinates:
                node = Node(coordinates[0], coordinates[1], node_type="blocking_node")
                path_to_tail_nodes.append(node)
            elif coordinates == last_tail_coordinate:
                target_tail_node = Node(coordinates[0], coordinates[1], node_type="target_node")
                path_to_tail_nodes.append(target_tail_node)
            else:
                path_to_tail_nodes.append(Node(coordinates[0], coordinates[1]))
        return self._get_path(self._start_node, target_tail_node, path_to_tail_nodes)

    def _decide_moving_direction(self, path_to_follow):
        first_step = path_to_follow.pop(0)
        if first_step.get_coordinates()[0] == self._start_node.get_coordinates()[0]:
            if first_step.get_coordinates()[1] > self._start_node.get_coordinates()[1]:
                self._snake.update_move_direction('down')
            else:
                self._snake.update_move_direction('up')
        else:
            if first_step.get_coordinates()[0] > self._start_node.get_coordinates()[0]:
                self._snake.update_move_direction('right')
            else:
                self._snake.update_move_direction('left')

        self._start_node.set_coordinates(*first_step.get_coordinates())  # Update _start_node to new Coordinates

    def think(self):

        if not self._path:
            self._create_real_path_nodes()
            self._path = self._get_path(self._start_node, self._target_node, self._nodes)
            self._path_back_exists = None

        if self._path:

            #########
            #self._gameField.tryout(500, 500)
            #########

            if not self._path_back_exists:
                self._path_back_exists = self._get_path_back_existance()

            if self._path_back_exists:
                self._path_to_tail = None
                self._decide_moving_direction(self._path)
            else:
                self._path = None
                print("No path BACK could be found, search path to TAIL")

                # if not self._path_to_tail:
                #     self._path_to_tail = self._get_path_to_tail()
                # if self._path_to_tail:
                #     print('Path to TAIL found!')
                #     print(self._path_to_tail)
                #     self._decide_moving_direction(self._path_to_tail)
                # else:
                #     # TODO
                #     print('I AM LOST!')
                #     pass
        else:
            self._path_back_exists = None
            print("NO PATH COULD BE FOUND, search path to TAIL")
            # if not self._path_to_tail:
            #     self._path_to_tail = self._get_path_to_tail()
            # if self._path_to_tail:
            #     print('Path to TAIL found!')
            #     print(self._path_to_tail)
            #     self._decide_moving_direction(self._path_to_tail)
            # else:
            #     # TODO
            #     print('I AM LOST!')
            #     pass

    def _create_real_path_nodes(self):
        playground = self._gameField.get_play_ground_positions()
        head_position = self._snake.get_head_position()
        tail_positions = self._snake.get_tail_positions()
        food_position = self._foodDispatcher.get_food_position()

        self._start_node = None
        self._target_node = None
        self._nodes = []

        for pos in playground:
            coordinates = self._gameField.map_pixels_to_coordinates(pos)
            if pos == head_position:
                self._start_node = Node(coordinates[0], coordinates[1], node_type="start_node")
                self._nodes.append(self._start_node)
            elif pos in tail_positions:
                node = Node(coordinates[0], coordinates[1], node_type="blocking_node")
                self._nodes.append(node)
            elif pos == food_position:
                self._target_node = Node(coordinates[0], coordinates[1], node_type="target_node")
                self._nodes.append(self._target_node)
            else:
                self._nodes.append(Node(coordinates[0], coordinates[1]))

    def _get_path(self, start_node, target_node, nodes):
        # TODO: Prefer paths near the wall or the snake itself
        open_list = list()
        closed_list = list()

        start_node.set_parent(None)

        start_node.set_head_distance(0)
        start_node.set_node_cost(0)
        open_list.append(start_node)

        while open_list:
            open_list.sort(key=lambda b: b.get_node_cost())  # TODO: Needed? / Use PriorityQueue
            current_node = open_list.pop(0)
            closed_list.append(current_node)
            if current_node.get_coordinates() == target_node.get_coordinates():
                path = []
                current = current_node
                while current is not None:
                    path.append(current)
                    current = current.get_parent()

                path = path[::-1]
                path.pop(0)
                return path

            for _next in self.searcher.get_neighbors(current_node, nodes):
                if _next in closed_list:
                    continue
                _next.set_parent(current_node)

                _next.set_head_distance(current_node.get_head_distance() + 10)
                _next.set_food_distance(self.searcher.get_heuristic_food_distance(_next))
                _next.set_node_cost(_next.get_head_distance() + _next.get_food_distance())

                if _next in open_list and _next.get_head_distance() >= current_node.get_food_distance():
                    continue
                open_list.append(_next)
        else:
            return False


    def greedy_walk(self):
        food_pos = self._foodDispatcher.get_food_position()
        food_pos_x = food_pos[0]
        food_pos_y = food_pos[1]
        head_pos = self._snake.get_head_position()
        head_pos_x = head_pos[0]
        head_pos_y = head_pos[1]
        move_dir = self._snake.get_move_direction()

        if not self._snake.get_move_direction():
            self._snake.update_move_direction('right')
            self._last_move_direction = 'right'

        if move_dir == "right":
            if food_pos_y < head_pos_y:
                self._snake.update_move_direction('up')
            elif food_pos_y > head_pos_y:
                self._snake.update_move_direction('down')
            elif food_pos_y == head_pos_y and food_pos_x < head_pos_x:
                self._snake.update_move_direction('down')
            else:
                print('RRR')
                pass

        elif move_dir == "left":
            if food_pos_y < head_pos_y:
                self._snake.update_move_direction('up')
            elif food_pos_y > head_pos_y:
                self._snake.update_move_direction('down')
            elif food_pos_y == head_pos_y and food_pos_x > head_pos_x:
                self._snake.update_move_direction('down')
            else:
                print('LLL')
                pass

        elif move_dir == "up":
            if food_pos_x < head_pos_x:
                self._snake.update_move_direction('left')
            elif food_pos_x > head_pos_x:
                self._snake.update_move_direction('right')
            elif food_pos_x == head_pos_x and food_pos_y > head_pos_y:
                self._snake.update_move_direction('right')
            else:
                print('UUU')
                pass

        elif move_dir == "down":
            if food_pos_x < head_pos_x:
                self._snake.update_move_direction('left')
            elif food_pos_x > head_pos_x:
                self._snake.update_move_direction('right')
            elif food_pos_x == head_pos_x and food_pos_y < head_pos_y:
                self._snake.update_move_direction('right')
            else:
                if food_pos_y < head_pos_y:
                    self._snake.update_move_direction('right')
                pass

    def _right_wall(self):
        return self._snake.get_head_position()[0] >= WINDOW_SIZE[0] - BLOCKSIZE - BORDER_SIZE

    def _left_wall(self):
        return self._snake.get_head_position()[0] <= BORDER_SIZE

    def _upper_wall(self):
        return self._snake.get_head_position()[1] <= 2*BLOCKSIZE

    def _lower_wall(self):
        return self._snake.get_head_position()[1] >= WINDOW_SIZE[1] - 3*BLOCKSIZE

    def _lower_wall_with_space(self):
        return self._snake.get_head_position()[1] >= WINDOW_SIZE[1] - 4*BLOCKSIZE