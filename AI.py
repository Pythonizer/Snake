
from Settings import BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE

from Searcher import Searcher

from Node import Node

from copy import deepcopy, copy


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

        print('-------')
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
        # TODO: Beware that one tail will appear after eat!
        virtual_free_coordinates = []
        virtual_blocking_coordinates = []
        if len(real_snake_coordinates) > len(virtual_path):
            # Set virtual target node
            v_target_index = len(virtual_path)-1
            v_target_coo = real_snake_coordinates[v_target_index]
            virtual_target_node = Node(v_target_coo[0], v_target_coo[1], node_type="target_node")

            # Make virtual moved snake free, except the virtual_target
            for i in range(0, len(virtual_path)-1):
                virtual_free_coordinates.append(real_snake_coordinates.pop(0))

            # Make remaining snake blocking, except the virtual_target
            start_of_blocking_snake = len(virtual_path)
            for i in range(start_of_blocking_snake, len(real_snake_coordinates)):
                virtual_blocking_coordinates.append(real_snake_coordinates[i])

            # Remove last node of path because its the real target/ virtual_start_node
            virtual_path.pop(-1)
            # The rest of the path is blocking
            for vp_node in virtual_path:
                virtual_blocking_coordinates.append(vp_node.get_coordinates())

            print('******')
            print('VBC: %s' % virtual_blocking_coordinates)
            print('VFC: %s' % virtual_free_coordinates)
            print('******')

        elif len(real_snake_coordinates)+1 < len(virtual_path):
            #print(len(real_snake_coordinates))
            v_target_index = len(virtual_path) - (len(real_snake_coordinates)+1)
            #v_target_index = len(virtual_path) - (len(real_tail_positions)+1)
            v_target_index = v_target_index - len(virtual_path)
            print('VTargetIndex: %s' % v_target_index)
            #print('VPath: %s' % virtual_path)
            virtual_target_node = deepcopy(virtual_path[v_target_index])
            virtual_target_node.set_node_type('target_node')

            for i, x in enumerate(virtual_path):
                if real_snake_coordinates:
                    virtual_free_coordinates.append(real_snake_coordinates.pop(0))
                    virtual_blocking_coordinates.append(virtual_path[-1*(i+1)].get_coordinates())
                else:
                    virtual_free_coordinates.append(x.get_coordinates())

        else:
            virtual_target_node = deepcopy(virtual_path[0])
            virtual_target_node.set_node_type('target_node')

        #print('VBlocking: %s' % virtual_blocking_coordinates)
        #print('VFree: %s' % virtual_free_coordinates)

        playground = self._gameField.get_play_ground()
        coordinate_playground = list(map(lambda c: self._gameField.map_pixels_to_coordinates(c), playground))
        for coordinates in coordinate_playground:

            if coordinates in virtual_free_coordinates:
                virtual_nodes.append(Node(coordinates[0], coordinates[1], node_type="free"))
            elif coordinates in coordinates in virtual_blocking_coordinates:
                virtual_nodes.append(Node(coordinates[0], coordinates[1], node_type="blocking_node"))

            elif coordinates == virtual_start_node.get_coordinates():
                virtual_nodes.append(virtual_start_node)

            elif coordinates == virtual_target_node.get_coordinates():
                virtual_nodes.append(virtual_target_node)
            else:

                virtual_nodes.append(Node(coordinates[0], coordinates[1]))

        #print('....')
        #print(virtual_nodes)
        #for n in virtual_nodes:
        #    if n.get_node_type() == 'target_node' or n.get_node_type() == 'start_node':
        #        print(n)
        #print('....')

        virtual_path_back = self._get_path(virtual_start_node, virtual_target_node, virtual_nodes)
        print('VStart: %s' % virtual_start_node)
        print('VTarget: %s' % virtual_target_node)
        #print('VPathBack: %s' % virtual_path_back)

        print('-------')
        return True if virtual_path_back else False

    def think(self):

        if not self._path:
            self._create_nodes()
            self._path = self._get_path(self._start_node, self._target_node, self._nodes)
            self._path_back = None

        if self._path:
            if not self._path_back:
                self._path_back = self._get_path_back()

            if self._path_back:  # Todo: check if path back exists, then:
            #if True:  # Todo: check if path back exists, then:
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