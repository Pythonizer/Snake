
import sys

import pygame

from old.Settings import BLOCKSIZE, BORDER_SIZE, WINDOW_SIZE


class GameField(object):

    def __init__(self, snake, screen):
        self._snake = snake
        self._screen = screen

        self._food_position = None

        self.clock = pygame.time.Clock()

    def tryout(self, x, y):
        print('ttttt')
        pygame.draw.circle(self._screen, (153,50,204), (x, y), 100, 10)
        self.clock.tick(500)
        pygame.draw.circle(self._screen, (153,50,204), (x, y), 10, 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.time.wait(500)
        pygame.display.update()
        pygame.time.wait(500)

    def get_game_field_block_size(self):
        return (WINDOW_SIZE[0] - (2*BLOCKSIZE)) // BLOCKSIZE, (WINDOW_SIZE[1] - (2*BLOCKSIZE))//BLOCKSIZE

    def update_food_position(self, pos):
        self._food_position = pos

    def get_play_ground_positions(self):
        play_ground = []
        for y in range(BORDER_SIZE, WINDOW_SIZE[1] - BORDER_SIZE, BLOCKSIZE):
            for x in range(BORDER_SIZE, WINDOW_SIZE[0] - BORDER_SIZE, BLOCKSIZE):
                play_ground.append((x, y))
        return play_ground

    def get_playground_coordinates(self):
        play_ground = []
        for y in range(0, (WINDOW_SIZE[1] - 2*BORDER_SIZE)//BLOCKSIZE):
            for x in range(0, (WINDOW_SIZE[1] - 2*BORDER_SIZE)//BLOCKSIZE):
                play_ground.append((x, y))
        return play_ground

    def get_free_space(self):
        snake_positions = self._snake.get_tail_positions()
        snake_positions.append(self._snake.get_head_position())

        free_playground = self.get_play_ground_positions()
        for snake_pos in snake_positions:
            try:
                free_playground.remove(snake_pos)
            except ValueError as err:
                print(err)
        return free_playground

    def map_pixels_to_coordinates(self, pixels):
        """

        (50, 50):   (0,0)
        (50, 80):   (0,1)
        (50, 110):  (0,2)

        :param pixels:
        :return:
        """
        return (int((pixels[0] // BLOCKSIZE) - 1), int((pixels[1] // BLOCKSIZE) - 1))

    def map_coordinates_to_pixles(self, coordinates):
        """
        (0,0)   (50,50)
        (0,1)   (50,80)
        (0,2)   (50,110)

        :param coordinates:
        :return:
        """
        return ((coordinates[0] + 1) * BLOCKSIZE, (coordinates[1] + 1) * BLOCKSIZE)

