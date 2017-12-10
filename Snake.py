import pygame

from Head import Head
from Tail import Tail
import Colors
from Settings import MOVE_STEP

#class Snake(pygame.sprite.Group):


class Snake(object):
    def __init__(self, pos_x, pos_y, size, color=Colors.GRASS_GREEN):
        super(Snake, self).__init__()
        self._color = color
        self._size = size

        self._position_x = pos_x
        self._position_y = pos_y
        self._move_direction = None

        self._head = Head(color=self._color, width=self._size, height=self._size, pos_x=self._position_x,
                          pos_y=self._position_y)
        #self._tails = pygame.sprite.Group()
        #self._group.add(self._head)
        #self._tail = Tail(Colors.GRASS_GREEN, self._size, self._size)
        self._tail = Tail()
        self._length = 0

    def get_color(self):
        return self._color

    def get_head_size(self):
        return self._size

    def get_head_position(self):
        #print "Head pos: %s, %s" % (self._position_x, self._position_y)
        return self._position_x, self._position_y

    def get_tail_positions(self):
        positions = []
        for t in self._tail:
            positions.append((t[0], t[1]))
        #print "Tail pos: %s" % positions
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
        #pygame.draw.rect(screen, self._color, self._head.rect)
        self._tail.draw(screen)
        self._head.draw(screen, self._move_direction)

    def eat(self):
        self._length += 1

    def _update_tail(self):
        #print self._tail
        # x=0
        # y=0
        # if self._move_direction == 'up':
        #     x=0
        #     y=20
        # elif self._move_direction == 'down':
        #     x=0
        #     y=-20
        # elif self._move_direction == 'left':
        #     x=20
        #     y=0
        # elif self._move_direction == 'right':
        #     x=-20
        #     y=0

        # Adding the actual position of the snakes head and removing the oldest tail element, if needed.
        #self._tail.add_tail_segment(self._position_x+x, self._position_y+y, self._move_direction)
        self._tail.add_tail_segment(self._position_x, self._position_y, self._move_direction)
        if self._length < len(self._tail):
            del self._tail[0]

