#!/usr/bin/env python

import pygame
from pygame import locals

from GameOverMenu import GameOverMenu
from StartMenu import StartMenu
from Snake import Snake
from FoodDispatcher import FoodDispatcher
import Colors
import sys
from datetime import datetime

HELP_CONTENT = 'HELP-MENU\n' \
               '----------\n' \
               'Shortcuts:\n' \
               '<space>: make screen-shot'\
               ''
FPS = 30
WINDOW_SIZE = 700, 700
FULLSCREEN = False
START_MENU_OPTIONS = ['1. Start Game', '2. Settings']
GAME_OVER_MENU_OPTIONS = ['1. Play again', '2. Quit']
MOVEMENT = None
MOVE_STEP = 10
BACKGORUND = Colors.BLACK
GAMEOVER = False

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    start_menu = StartMenu(screen, START_MENU_OPTIONS)
    start_menu.run()
    game_over_menu = GameOverMenu(screen, GAME_OVER_MENU_OPTIONS)

    snake = Snake(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2)
    food_dispatcher = FoodDispatcher(screen, (0, 0), WINDOW_SIZE)

    while not GAMEOVER:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == locals.MOUSEBUTTONDOWN:
                print (pygame.mouse.get_pos())
            elif event.type == locals.KEYDOWN:
                    if event.key == locals.K_q or event.key == locals.K_ESCAPE:
                        sys.exit()

                    elif event.key == locals.K_f:
                        if not FULLSCREEN:
                            screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode(WINDOW_SIZE)
                        FULLSCREEN = not FULLSCREEN
                    elif event.key == locals.K_h:
                        print HELP_CONTENT
                    elif event.key == locals.K_SPACE:
                        pygame.image.save(screen, 'screenshots/screenshot_%s.png' % str(datetime.now()))

                    elif event.key == pygame.K_LEFT and snake.get_move_direction() != 'right':
                        print "left"
                        snake.update_move_direction('left')
                    elif event.key == pygame.K_RIGHT and snake.get_move_direction() != 'left':
                        print "right"
                        snake.update_move_direction('right')
                    elif event.key == pygame.K_UP and snake.get_move_direction() != 'down':
                        print "up"
                        snake.update_move_direction('up')
                    elif event.key == pygame.K_DOWN and snake.get_move_direction() != 'up':
                        print "down"
                        snake.update_move_direction('down')

                    #todo tryout
                    elif event.key == pygame.K_1:
                        snake.eat()

        # Update snake
        screen.fill(BACKGORUND)
        food_dispatcher.draw()
        snake.move(MOVE_STEP)
        snake.draw(screen)


        # Logic
        if snake.get_position()[0] < 0 or snake.get_position()[0] >= WINDOW_SIZE[0] \
                or snake.get_position()[1] < 0 or snake.get_position()[1] >= WINDOW_SIZE[1]:
            GAMEOVER = game_over_menu.run()
            if not GAMEOVER:
                del(snake)
                snake = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)

            print GAMEOVER

        pygame.display.flip()
