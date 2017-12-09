import pygame

from Head import Head
from Tail import Tail
import Colors

#class Snake(pygame.sprite.Group):

class Snake(object):
    def __init__(self, pos_x, pos_y, color=Colors.GRASS_GREEN, size=30):
        super(Snake, self).__init__()
        self._color = color
        self._size = size

        self._position_x = pos_x
        self._position_y = pos_y
        self._move_direction = None

        self._head = Head(color=self._color, width=self._size, height=self._size, pos_x=self._position_x,
                          pos_y=self._position_y)
        self._tails = pygame.sprite.Group()
        #self._group.add(self._head)

    def get_color(self):
        return self._color

    def get_position(self):
        return self._position_x, self._position_y

    def update_move_direction(self, direction):
        self._move_direction = direction

    def get_move_direction(self):
        return self._move_direction

    def move(self, step):
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
        pygame.draw.rect(screen, self._color, self._head.rect)
        self._tails.draw(screen)

    def eat(self):
        self._add_tail()

    def _add_tail(self):
        print self._tails
        for element in self._tails:
            print element
        self._tails.add(Tail((100,100,100), self._size, self._size, pos_x=(self._head.get_pos_x()),
                             pos_y=self._head.get_pos_y()))
