import pygame
import random
from Settings import MOVE_STEP, BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE
from Food import Food


class FoodDispatcher(object):
    def __init__(self, screen, min_range, max_range, snake):  # todo: handle snake connection differently
        self._screen = screen
        self._min_x = min_range[0]
        self._min_y = min_range[1]
        self._max_x = max_range[0]
        self._max_y = max_range[1]

        self.snake = snake

        self._food = None

        self.place_food()
        self.remove_food()
        self.place_food()

    # TODO use map/ lambda etc for this
    def _get_play_ground(self):
        play_ground = []
        for i in range(BORDER_SIZE, WINDOW_SIZE[0]-BORDER_SIZE, BLOCKSIZE):
            for j in range(BORDER_SIZE, WINDOW_SIZE[1]-BORDER_SIZE, BLOCKSIZE):
                play_ground.append((i, j))
        return play_ground

    def _get_free_placing_space(self):
        snake_positions = self.snake.get_tail_positions()
        snake_positions.append(self.snake.get_head_position())

        playground = self._get_play_ground()
        for snake_pos in snake_positions:
            playground.remove(snake_pos)

        return playground

    def place_food(self):
        free_space = self._get_free_placing_space()
        if not self._food:
            self._food = Food('random', 0, 0)
        # ValueError: empty range for randrange() (0,0, 0)
        rand_pos = free_space[random.randint(0, len(free_space)-1)]
        self._food.update_x_position(rand_pos[0])
        self._food.update_y_position(rand_pos[1])

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
