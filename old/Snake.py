from Head import Head
from Tail import Tail

from old import Colors


class Snake(object):
    def __init__(self, pos_x, pos_y):
        super(Snake, self).__init__()

        self._position_x = pos_x
        self._position_y = pos_y
        self._move_direction = None

        self._head = Head(pos_x=self._position_x, pos_y=self._position_y)
        self._tail = Tail()
        self._length = 0

        self._last_moved_tail_pos = None

        # Start with tail length of 1?
        #self.eat()
        #self._update_tail()

    def get_head(self):
        return self._head

    def get_head_position(self):
        return self._position_x, self._position_y

    def get_tail_positions(self):
        positions = []
        for t in self._tail:
            positions.append((t[0], t[1]))
        return positions

    def update_move_direction(self, direction):
        self._move_direction = direction

    def get_move_direction(self):
        return self._move_direction

    def move(self, step):
        self._update_tail()
        if self._move_direction == 'up':
            self._position_y -= step
            self._head.update_y_position(self._position_y)
        elif self._move_direction == 'down':
            self._position_y += step
            self._head.update_y_position(self._position_y)
        elif self._move_direction == 'left':
            self._position_x -= step
            self._head.update_x_position(self._position_x)
        elif self._move_direction == 'right':
            self._position_x += step
            self._head.update_x_position(self._position_x)

    def draw(self, screen):
        self._tail.draw(screen)
        self._head.draw(screen, self._move_direction)

    def eat(self):
        self._length += 1
        #print(self._last_moved_tail_pos)

    def _update_tail(self):
        self._tail.add_tail_segment(self._position_x, self._position_y, self._move_direction)
        if self._length < len(self._tail):
            self._last_moved_tail_pos = self._tail[0][0], self._tail[0][1]  # TODO: last moved snake position
            del self._tail[0]

