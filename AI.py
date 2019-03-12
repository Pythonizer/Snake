
from Settings import BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE

from Searcher import Searcher

from Node import Node

from copy import copy


class AI(object):
    def __init__(self, snake, food_dispatcher, gameField):
        self._snake = snake
        self._foodDispatcher = food_dispatcher
        self._gameField = gameField
        self._last_move_direction = None

        self.searcher = Searcher(gameField, snake, food_dispatcher)

        self._path = None
        self._path_back = None
        self._start_node = None
        self._target_node = None
        self._nodes = None

    def _get_path_back(self):
        virtual_path = copy(self._path)
        virtual_start_node = copy(self._start_node)
        virtual_start_node.set_coordinates(*virtual_path[-1].get_coordinates())

        print('sdfsf')

        tail_positions = self._snake.get_tail_positions()

        for t in tail_positions:
            print(t)
        print("--------")
        """
        (410.0, 380.0)
        (380.0, 380.0)
        (350.0, 380.0)
        (320.0, 380.0)
        (290.0, 380.0)
        (260.0, 380.0)
        (230.0, 380.0)
        # Next would be head
        """

        #for p in virtual_path:
        #    print(p)

        return True  # TODO

    def think(self):

        if not self._path:
            self._create_nodes()
            self._path = self._get_path(self._start_node, self._target_node, self._nodes)

        if self._path:
            if not self._path_back:
                self._path_back = self._get_path_back()

            if self._path_back:  # Todo: check if path back exists, then:
                first_step = self._path.pop(0)
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
            else:
                print("No path BACK could be found")
        else:
            print("NO PATH COULD BE FOUND")
            # TODO: What then

    def _create_nodes(self):
        playground = self._gameField.get_play_ground()
        head_position = self._snake.get_head_position()
        tail_positions = self._snake.get_tail_positions()
        food_position = self._foodDispatcher.get_food_position()

        for t in tail_positions:
            print(t)
        print("--------")
        print(head_position)
        print("--------")

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
        # TODO: Prefere paths near the wall or the snake itself
        open_list = list()
        closed_list = list()

        start_node.set_parent(None)

        start_node.set_head_distance(0)
        start_node.set_node_cost(0)
        open_list.append(start_node)

        while open_list:
            open_list.sort(key=lambda b: b.get_node_cost()) # TODO: Needed? / Use PriorityQueue
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