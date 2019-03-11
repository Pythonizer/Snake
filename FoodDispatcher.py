import pygame
import random
from Settings import MOVE_STEP, BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE
from Food import Food


class FoodDispatcher(object):
    def __init__(self, screen, gameField):  # todo: handle snake connection differently
        self._screen = screen
        self.gameField = gameField

        self._food = None

        self.place_food()
        self.remove_food()
        self.place_food()

    def place_food(self):
        free_space = self.gameField.get_free_space()
        if not self._food:
            self._food = Food('random', 0, 0)
        # ValueError: empty range for randrange() (0,0, 0)
        rand_pos = free_space[random.randint(0, len(free_space)-1)]
        self._food.update_x_position(rand_pos[0])
        self._food.update_y_position(rand_pos[1])
        self._food.update_food_type('random')

        self.gameField.update_food_position(rand_pos)

    def remove_food(self):
        self._food = None

    def get_food_position(self):
        if self._food:
            return self._food.get_pos_x(), self._food.get_pos_y()

    def get_food_coordinates(self):
        return self.gameField.map_pixels_to_coordinates(self.get_food_position())

    def get_food_size(self):
        return self._food.get_size()

    def draw(self):
        if self._food:
            self._food.draw(self._screen)
