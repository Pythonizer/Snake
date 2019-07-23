

class Node:

    def __init__(self, coordinate_x, coordinate_y, node_type="free"):

        self._coordinate_x = coordinate_x
        self._coordinate_y = coordinate_y

        self._node_type = node_type

        self._dist_start = None
        self._dist_target = None
        self._node_cost = None

        self._node_location = 'free'
        #self._location_cost_mapper = {'free': 0,
        #                              'near_snake': 0.5,
        #                              'near_wall': 0.8}

        self._parent = None

        #self._update_location()

    def get_coordinates(self):
        return self._coordinate_x, self._coordinate_y

    def set_start_distance(self, dist):
        self._dist_start = dist

    def get_start_distance(self):
        return self._dist_start

    def set_target_distance(self, dist):
        self._dist_target = dist

    def get_target_distance(self):
        return self._dist_target

    def set_node_cost(self, cost):
        self._node_cost = cost

    def get_node_cost(self):
        return self._node_cost

    #def get_location_weighted_cost(self):
    #    return self.get_node_cost() - self._location_cost_mapper[self._node_location]

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
        #self._update_location()

    def set_node_type(self, node_type):
        """
        Just used for virtual path
        :param node_type:
        :return:
        """
        self._node_type = node_type

    # def _update_location(self):
    #     if self._coordinate_x == 0 or self._coordinate_x == 19\
    #             or self._coordinate_y == 0 or self._coordinate_y == 19:
    #         self._node_location = 'near_wall'
    #     elif False:  # TODO: Handle near snake distance
    #         pass
    #     else:
    #         self._node_location = 'free'

    def __repr__(self):
        return "Node(coordinate_x={c1}, coordinate_y={c2}, node_type='{n_type}'".format(c1=self._coordinate_x,
                                                                                        c2=self._coordinate_y,
                                                                                        n_type=self._node_type)
