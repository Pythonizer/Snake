import pygame
import random
from Settings import MOVE_STEP, BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE
from Food import Food


class FoodDispatcher(object):
    def __init__(self, screen, min_range, max_range, snake, gameField):  # todo: handle snake connection differently
        self._screen = screen
        self._min_x = min_range[0]
        self._min_y = min_range[1]
        self._max_x = max_range[0]
        self._max_y = max_range[1]

        self.snake = snake
        self.gameField = gameField

        self._food = None

        self.place_food()
        self.remove_food()
        self.place_food()

    def place_food(self):
        #free_space = self._get_free_placing_space()
        free_space = self.gameField.get_free_space()
        if not self._food:
            self._food = Food('random', 0, 0)
        # ValueError: empty range for randrange() (0,0, 0)
        rand_pos = free_space[random.randint(0, len(free_space)-1)]
        self._food.update_x_position(rand_pos[0])
        self._food.update_y_position(rand_pos[1])
        self._food.update_food_type('random')

        self.gameField.update_food_position(rand_pos)

        #print self.snake.get_head_position()
        #print rand_pos

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
