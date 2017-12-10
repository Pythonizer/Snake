import pygame
import random
from Apple import Apple
from Settings import MOVE_STEP


class FoodDispatcher(object):
    def __init__(self, screen, min_range, max_range):
        self._screen = screen
        self._min_x = min_range[0]
        self._min_y = min_range[1]
        self._max_x = max_range[0]
        self._max_y = max_range[1]

        self._food = None

        self.place_food()
        self.remove_food()
        self.place_food()

    def place_food(self):
        if not self._food:
            self._food = Apple(0, 0)
        # Round coordinates to keep it aligned to the snakes movement
        x = random.randrange(self._min_x, self._max_x - self._food.get_size())
        rounded_x = round(x/MOVE_STEP)*MOVE_STEP
        y = random.randrange(self._min_y, self._max_y - self._food.get_size())
        rounded_y = round(y/MOVE_STEP)*MOVE_STEP
        self._food.update_x_position(rounded_x)
        self._food.update_y_position(rounded_y)

    def remove_food(self):
        self._food = None

    def get_food_position(self):
        if self._food:
            return self._food.get_pos_x(), self._food.get_pos_y()

    def get_food_size(self):
        return self._food.get_size()

    def draw(self):
        #pygame.draw.rect(self._screen, self._food.get_color(), self._food.rect)
        if self._food:
            self._food.draw(self._screen)
