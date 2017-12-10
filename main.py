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

from Settings import FPS, WINDOW_SIZE, FULLSCREEN, START_MENU_OPTIONS, GAME_OVER_MENU_OPTIONS, MOVE_STEP
from Settings import BACKGORUND, GAMEOVER, BLOCKSIZE, HELP_CONTENT, BACKGROUND_IMG, BORDER_SIZE

QUIT = False

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    background_image = pygame.image.load(BACKGROUND_IMG)

    start_menu = StartMenu(screen, START_MENU_OPTIONS)
    start_menu.run()
    game_over_menu = GameOverMenu(screen, GAME_OVER_MENU_OPTIONS)

    snake = Snake(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2, size=BLOCKSIZE)
    food_dispatcher = FoodDispatcher(screen, (BORDER_SIZE, BORDER_SIZE),
                                     (WINDOW_SIZE[0]-BORDER_SIZE, WINDOW_SIZE[1]-BORDER_SIZE))

    while not QUIT:
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
                    elif event.key == pygame.K_2:
                        #food_dispatcher.remove_food()
                        food_dispatcher.place_food()


        # Update snake
        screen.fill(BACKGORUND)
        screen.blit(background_image, (0, 0))
        food_dispatcher.draw()
        snake.move(MOVE_STEP)
        snake.draw(screen)

        food_pos_x = food_dispatcher.get_food_position()[0]
        food_pos_y = food_dispatcher.get_food_position()[1]
        food_size = food_dispatcher.get_food_size()
        head_pos_x = snake.get_head_position()[0]
        head_pos_y = snake.get_head_position()[1]
        head_size = snake.get_head_size()

        # Logic
        if snake.get_head_position()[0] < BORDER_SIZE or snake.get_head_position()[0] > WINDOW_SIZE[0]-BLOCKSIZE-BORDER_SIZE \
                or snake.get_head_position()[1] < BLOCKSIZE or snake.get_head_position()[1] > WINDOW_SIZE[1]-BLOCKSIZE-BLOCKSIZE:
            GAMEOVER = True
        for tail_segment_pos in snake.get_tail_positions():
            if snake.get_head_position()[0] == tail_segment_pos[0] and snake.get_head_position()[1] == tail_segment_pos[1]:
                GAMEOVER = True

        if GAMEOVER:
            QUIT = game_over_menu.run()
            if not QUIT:
                del(snake)
                snake = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, BLOCKSIZE)
                GAMEOVER = False

        elif snake.get_head_position()[0] == food_dispatcher.get_food_position()[0]\
                and snake.get_head_position()[1] == food_dispatcher.get_food_position()[1]:
            pass

        elif food_pos_x <= head_pos_x <= food_pos_x+food_size and food_pos_y <= head_pos_y <= food_pos_y+food_size\
                or food_pos_x <= head_pos_x+head_size <= food_pos_x+food_size and food_pos_y <= head_pos_y+head_size <= food_pos_y+food_size:
            print "Eat that shit"
            #food_dispatcher.remove_food()
            snake.eat()
            food_dispatcher.remove_food()
            food_dispatcher.place_food()

        pygame.display.flip()
