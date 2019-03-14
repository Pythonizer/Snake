

class Node:

    def __init__(self, coordinate_x, coordinate_y, node_type="free"):

        self._coordinate_x = coordinate_x
        self._coordinate_y = coordinate_y

        self._node_type = node_type

        self._dist_head = None
        self._dist_food = None
        self._node_cost = None

        self._parent = None

    def get_coordinates(self):
        return self._coordinate_x, self._coordinate_y

    def set_head_distance(self, dist):
        self._dist_head = dist

    def get_head_distance(self):
        return self._dist_head

    def set_food_distance(self, dist):
        self._dist_food = dist

    def get_food_distance(self):
        return self._dist_food

    def set_node_cost(self, cost):
        self._node_cost = cost

    def get_node_cost(self):
        return self._node_cost

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def get_node_type(self):
        return self._node_type

    def set_coordinates(self, x, y):
        """
        Just used for virtual path
        :param x:
        :param y:
        :return:
        """
        self._coordinate_x = x
        self._coordinate_y = y

    def set_node_type(self, node_type):
        """
        Just used for virtual path
        :param node_type:
        :return:
        """
        self._node_type = node_type

    def __repr__(self):
        return "Node(coordinate_x={c1}, coordinate_y={c2}, node_type='{n_type}'".format(c1=self._coordinate_x,
                                                                                        c2=self._coordinate_y,
                                                                                        n_type=self._node_type)
