import uuid
import pprint


class BlockHandler(object):
    def __init__(self, nbr_x, nbr_y, gameField):
        self._nbr_x = nbr_x
        self._nbr_y = nbr_y
        self._gameField = gameField

        self._blocks = []

        self._create_blocks()

    def _create_blocks(self):
        for x in range(0, self._nbr_x-1):
            for y in range(0, self._nbr_y-1):
                x_pos, y_pos = self._gameField.map_coordinates_to_pixles((x, y))
                self._blocks.append(GameFieldBlock(x, y, x_pos, y_pos))

    def get_blocks(self):
        return self._blocks

    def update_blocks(self, snake_positions, fruit_pos):
        def test(block, b_type):
            block.set_type(b_type)
            return block

        self._blocks = []

        #self[:] = [b.set_type("tail") if b.get_position() in snake_positions else b.set_type("free") for b in self]
        #self[:] = [b for b in self]
        #self[:] = list(map(lambda b: b.set_type("tail") if b.get_position() in snake_positions else b.set_type("free"), self))
        #list(map(lambda b: b.set_type("tail") if b.get_position() in snake_positions else b.set_type("free"), self))
        list(map(lambda b: self._blocks.append(test(b, "tail")) if b.get_position() in snake_positions else self._blocks.append(test(b, "free")), self._blocks))
        print(self)

    def get_block_by_id(self, id):
        pass

    def get_block_by_coordinates(self, coordinates):
        print(coordinates)
        for b in self._blocks:
            if coordinates == b.get_coordinates():
                return b

    def get_block_by_positions(self, positions):
        for b in self._blocks:
            if positions == b.get_position():
                return b

    def __repr__(self):
        ret_str = ""
        count = 1
        for b in self._blocks:
            cx, cy = b.get_coordinates()
            ret_str += "GameFieldBlock({}, {}, {}) ".format(cx, cy, b.get_block_type())
            #ret_str += "({}, {}) ".format(cx, cy)
            if count % 20 == 0:
                ret_str += "\n"
            count += 1
        return ret_str


class GameFieldBlock(object):
    def __init__(self, x_coordinate, y_coordinate, x_pos, y_pos):
        self._x_coordinate = x_coordinate
        self._y_coordinate = y_coordinate
        self._x_pos = x_pos
        self._y_pos = y_pos
        self._dist_head = -1
        self._dist_food = -1
        self._dist_sum = -1

        self._block_type = "free"
        self._uid = uuid.uuid4()

    def __repr__(self):
        return "GameFieldBlock({}, {}, {})".format(self._x_coordinate, self._y_coordinate, self._block_type)

    def get_position(self):
        return self._x_pos, self._y_pos

    def get_coordinates(self):
        return self._x_coordinate, self._y_coordinate

    def set_head_distance(self, dist):
        self._dist_head = dist

    def set_food_distance(self, dist):
        self._dist_food = dist

    def get_dist_sum(self):
        return self._dist_food + self._dist_head

    def set_type(self, block_type):
        """
        free, head, tail, food
        :param block_type:
        :return:
        """
        self._block_type = block_type

    def get_block_type(self):
        return self._block_type

    def get_id(self):
        return self._uid


class BorderBlock(object):
    def __init__(self):
        pass