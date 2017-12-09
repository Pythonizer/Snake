import pygame
import random
from Apple import Apple


class FoodDispatcher(object):
    def __init__(self, screen, min_range, max_range):
        self._screen = screen
        self._min_x = min_range[0]
        self._min_y = min_range[1]
        self._max_x = max_range[0]
        self._max_y = max_range[1]

        self._fruit = None

        self.place_food()

    def place_food(self):
        if not self._fruit:
            self._fruit = Apple(0, 0)
            self._fruit.update_x_position(random.randrange(self._min_x, self._max_x - self._fruit.get_size()))
            self._fruit.update_y_position(random.randrange(self._min_y, self._max_y - self._fruit.get_size()))

    def draw(self):
        pygame.draw.rect(self._screen, self._fruit._color, self._fruit.rect)
