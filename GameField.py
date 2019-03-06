
import pygame
import random
from Settings import MOVE_STEP, BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE
from BlockHandling import GameFieldBlock


class GameField(object):

    def __init__(self, snake):
        self._snake = snake

        self._food_position = None

    def get_game_field_block_size(self):
        return (WINDOW_SIZE[0] - (2*BLOCKSIZE)) // BLOCKSIZE, (WINDOW_SIZE[1] - (2*BLOCKSIZE))//BLOCKSIZE

    def update_food_position(self, pos):
        self._food_position = pos

    # TODO use map/ lambda etc for this
    def get_play_ground(self):
        play_ground = []
        #for i in range(BORDER_SIZE, WINDOW_SIZE[0] - BORDER_SIZE, BLOCKSIZE):
        #    for j in range(BORDER_SIZE, WINDOW_SIZE[1] - BORDER_SIZE, BLOCKSIZE):
        for y in range(BORDER_SIZE, WINDOW_SIZE[1] - BORDER_SIZE, BLOCKSIZE):
            for x in range(BORDER_SIZE, WINDOW_SIZE[0] - BORDER_SIZE, BLOCKSIZE):
                play_ground.append((x, y))
        return play_ground

    def get_free_space(self):
        snake_positions = self._snake.get_tail_positions()
        snake_positions.append(self._snake.get_head_position())

        playground = self.get_play_ground()
        for snake_pos in snake_positions:
            try:
                playground.remove(snake_pos)
            except ValueError as err:
                # TODO: why?
                # ToDo: appears just after "play again"/ first element eaten
                print("*******")
                print(str(err))
                print("SnakePos: %s" % str(snake_pos))
                print("Playground: %s" % str(playground))
                print("*******")

        return playground

    # def get_game_matrix(self):
    #     """
    #
    #     Free space:     0
    #     Tail:           1
    #     Head:           2
    #     Food:           3
    #
    #
    #     :return:
    #     """
    #     play_ground = self.get_play_ground()
    #     #free_space = self.get_free_space()
    #     tail_positions = self._snake.get_tail_positions()
    #     head_position = self._snake.get_head_position()
    #     food_position = self._food_position
    #     matrix = []
    #     play_ground_index = 0
    #     # Todo: use lambda?
    #     for y in xrange(0, 20):
    #         matrix.append([])
    #         for x in xrange(0, 20):
    #             if play_ground[play_ground_index] == head_position:
    #                 matrix[y].append(2)
    #             elif play_ground[play_ground_index] == food_position:
    #                 matrix[y].append(3)
    #             elif play_ground[play_ground_index] in tail_positions:
    #                 matrix[y].append(1)
    #             else:
    #                 matrix[y].append(0)
    #             play_ground_index += 1
    #
    #     return matrix

    def map_pixels_to_coordinates(self, pixels):
        """

        (50, 50):   (0,0)
        (50, 80):   (0,1)
        (50, 110):  (0,2)

        :param pixels:
        :return:
        """
        return ((pixels[0] / BLOCKSIZE) - 1, (pixels[1] / BLOCKSIZE) - 1)

    def map_coordinates_to_pixles(self, coordinates):
        return ((coordinates[0] + 1) * BLOCKSIZE, (coordinates[1] + 1) * BLOCKSIZE)

