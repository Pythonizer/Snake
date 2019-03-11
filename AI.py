
from Settings import BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE

from Searcher import Searcher

from Node import Node


class AI(object):
    def __init__(self, snake, food_dispatcher, gameField):
        self._snake = snake
        self._foodDispatcher = food_dispatcher
        self._gameField = gameField
        self._last_move_direction = None

        self.searcher = Searcher(gameField, snake, food_dispatcher)

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

    def _get_path(self, start_node, target_node, nodes):
        open_list = list()
        closed_list = list()

        start_node.set_parent(None)

        start_node.set_head_distance(0)
        start_node.set_node_cost(0)
        open_list.append(start_node)

        while open_list:
            open_list.sort(key=lambda b: b.get_node_cost())
            current_node = open_list.pop(0)
            closed_list.append(current_node)
            if current_node.get_coordinates() == target_node.get_coordinates():
                print("DOOOOOOOONNNNNEEEEEE")
                # TODO: backtrack function?
                path = []
                current = current_node
                while current is not None:
                    path.append(current)
                    current = current.get_parent()
                return path[::-1]

            for _next in self.searcher.get_neighbors(current_node, nodes):
                if _next in closed_list:
                    continue

                _next.set_parent(current_node)

                _next.set_head_distance(current_node.get_head_distance() + 1)
                _next.set_food_distance(self.searcher.get_heuristic_food_distance(_next))  # TODO
                _next.set_node_cost(_next.get_head_distance() + _next.get_food_distance())

                if _next in open_list and _next.get_head_distance() >= current_node.get_food_distance():
                    continue
                open_list.append(_next)

    def think(self):

        playground = self._gameField.get_play_ground()
        head_position = self._snake.get_head_position()
        tail_positions = self._snake.get_tail_positions()
        food_position = self._foodDispatcher.get_food_position()

        start_node = None
        target_node = None

        nodes = []
        for pos in playground:
            coordinates = self._gameField.map_pixels_to_coordinates(pos)
            if pos == head_position:
                start_node = Node(coordinates[0], coordinates[1], node_type="start_node")
                nodes.append(start_node)
            elif pos in tail_positions:
                node = Node(coordinates[0], coordinates[1], node_type="blocking_node")
                nodes.append(node)
            elif pos == food_position:
                target_node = Node(coordinates[0], coordinates[1], node_type="target_node")
                nodes.append(target_node)
            else:
                node = Node(coordinates[0], coordinates[1])
                nodes.append(node)

        path = self._get_path(start_node, target_node, nodes)

        print('*********************')
        print("Start node: %s" % start_node)
        print("Target node: %s" % target_node)
        print("Path: %s" % path)
        print('*********************')

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
