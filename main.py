#!/usr/bin/env python

import pygame
from pygame import locals

from GameOverMenu import GameOverMenu
from StartMenu import StartMenu
from Snake import Snake
from FoodDispatcher import FoodDispatcher
from AI import AI
from GameField import GameField
import Colors
import sys
from datetime import datetime
from pprint import pprint

import math

from Settings import FPS, WINDOW_SIZE, FULLSCREEN, START_MENU_OPTIONS, GAME_OVER_MENU_OPTIONS, MOVE_STEP
from Settings import BACKGORUND, GAMEOVER, BLOCKSIZE, HELP_CONTENT, BACKGROUND_IMG, BORDER_SIZE

QUIT = False

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)

    background_image = pygame.image.load(BACKGROUND_IMG)

    start_menu = StartMenu(screen, START_MENU_OPTIONS)
    game_mode = start_menu.run()
    game_over_menu = GameOverMenu(screen, GAME_OVER_MENU_OPTIONS)

    snake = Snake(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2, size=BLOCKSIZE)

    gameField = GameField(snake)
    foodDispatcher = FoodDispatcher(screen, (BORDER_SIZE, BORDER_SIZE),
                                    (WINDOW_SIZE[0]-BORDER_SIZE, WINDOW_SIZE[1]-BORDER_SIZE), snake, gameField)

    ai = AI(snake, foodDispatcher, gameField)

    while not QUIT:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == locals.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
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
                    print(HELP_CONTENT)
                elif event.key == locals.K_SPACE:
                    pygame.image.save(screen, 'screenshots/screenshot_%s.png' % str(datetime.now()))


                    #todo tryout
                elif event.key == pygame.K_1:
                    snake.eat()
                elif event.key == pygame.K_2:
                    #food_dispatcher.remove_food()
                    foodDispatcher.place_food()
                elif event.key == pygame.K_3:
                    print(ai.searcher.get_relative_head_to_fruit_distance())
                    print(ai.searcher.get_relative_point_to_fruit_distance((0, 0)))
                elif event.key == pygame.K_4:
                    ai.test()
                elif event.key == pygame.K_5:
                    ai.test2()
                elif event.key == pygame.K_6:
                    print("Snake head: {head_pos}".format(head_pos=snake.get_head_position()))

                if game_mode == 'player':
                    if event.key == pygame.K_LEFT and snake.get_move_direction() != 'right':
                        print("left")
                        snake.update_move_direction('left')
                    elif event.key == pygame.K_RIGHT and snake.get_move_direction() != 'left':
                        print("right")
                        snake.update_move_direction('right')
                    elif event.key == pygame.K_UP and snake.get_move_direction() != 'down':
                        print("up")
                        snake.update_move_direction('up')
                    elif event.key == pygame.K_DOWN and snake.get_move_direction() != 'up':
                        print("down")
                        snake.update_move_direction('down')
        if game_mode == 'ai':
            #ai.tryout()
            #ai.tryout_wall()
            #ai.simple_walk()
            ai.greedy_walk()

        # Update snake
        screen.fill(BACKGORUND)
        screen.blit(background_image, (0, 0))
        foodDispatcher.draw()
        snake.move(MOVE_STEP)
        snake.draw(screen)

        food_pos_x = foodDispatcher.get_food_position()[0]
        food_pos_y = foodDispatcher.get_food_position()[1]
        food_size = foodDispatcher.get_food_size()
        head_pos_x = snake.get_head_position()[0]
        head_pos_y = snake.get_head_position()[1]
        head_size = snake.get_head_size()

        #print food_pos_x, food_pos_y
        #print head_pos_x, head_pos_x
        #print ''

        # ******** Logic ********
        if head_pos_x < BORDER_SIZE or head_pos_x > WINDOW_SIZE[0]-BLOCKSIZE-BORDER_SIZE \
                or head_pos_y < BLOCKSIZE or head_pos_y > WINDOW_SIZE[1]-BLOCKSIZE-BLOCKSIZE:
            GAMEOVER = True
        for tail_segment_pos in snake.get_tail_positions():
            if head_pos_x == tail_segment_pos[0] and head_pos_y == tail_segment_pos[1]:
                GAMEOVER = True

        if GAMEOVER:
            QUIT = game_over_menu.run()
            if not QUIT:
                del(snake)
                snake = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, BLOCKSIZE)
                ai = AI(snake, foodDispatcher, gameField)
                GAMEOVER = False

        elif food_pos_x == head_pos_x and food_pos_y == head_pos_y:
            print("Eat that shit")
            #food_dispatcher.remove_food()
            snake.eat()
            foodDispatcher.remove_food()
            foodDispatcher.place_food()

        #pygame.display.flip()
        pygame.display.update()
