
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


from Settings import FPS, WINDOW_SIZE, FULLSCREEN, START_MENU_OPTIONS, GAME_OVER_MENU_OPTIONS, MOVE_STEP
from Settings import BACKGORUND, BLOCKSIZE, HELP_CONTENT, BACKGROUND_IMG, BORDER_SIZE


class Game:

    def __init__(self):
        pygame.init()
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(WINDOW_SIZE)

        self._full_screen = FULLSCREEN

        self._background_image = pygame.image.load(BACKGROUND_IMG)

        start_menu = StartMenu(self._screen, START_MENU_OPTIONS)
        self._game_mode = start_menu.run()
        self._game_over_menu = GameOverMenu(self._screen, GAME_OVER_MENU_OPTIONS)

        self._snake = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, size=BLOCKSIZE)

        self._gameField = GameField(self._snake)
        self._foodDispatcher = FoodDispatcher(self._screen, (BORDER_SIZE, BORDER_SIZE),
                                        (WINDOW_SIZE[0] - BORDER_SIZE, WINDOW_SIZE[1] - BORDER_SIZE), self._gameField)

        self._ai = AI(self._snake, self._foodDispatcher, self._gameField)

        self._quit = False

    def _update_snake(self):
        # Update snake
        self._screen.fill(BACKGORUND)
        self._screen.blit(self._background_image, (0, 0))
        self._foodDispatcher.draw()
        self._snake.move(MOVE_STEP)
        self._snake.draw(self._screen)

    def _is_gameover(self):
        head_pos_x = self._snake.get_head_position()[0]
        head_pos_y = self._snake.get_head_position()[1]

        # ******** Logic ********
        if head_pos_x < BORDER_SIZE or head_pos_x > WINDOW_SIZE[0] - BLOCKSIZE - BORDER_SIZE \
                or head_pos_y < BLOCKSIZE or head_pos_y > WINDOW_SIZE[1] - BLOCKSIZE - BLOCKSIZE:
            return True
        for tail_segment_pos in self._snake.get_tail_positions():
            if head_pos_x == tail_segment_pos[0] and head_pos_y == tail_segment_pos[1]:
                return True
        return False

    def _check_eating(self):
        food_pos_x = self._foodDispatcher.get_food_position()[0]
        food_pos_y = self._foodDispatcher.get_food_position()[1]
        head_pos_x = self._snake.get_head_position()[0]
        head_pos_y = self._snake.get_head_position()[1]

        if food_pos_x == head_pos_x and food_pos_y == head_pos_y:
                print("Eat that shit")
                self._snake.eat()
                self._foodDispatcher.remove_food()
                self._foodDispatcher.place_food()

    def _handle_game_interactions(self, event):
        if event.key == locals.K_q or event.key == locals.K_ESCAPE:
            sys.exit()

        elif event.key == locals.K_f:
            if not self._full_screen:
                self._screen = pygame.display.set_mode(WINDOW_SIZE, pygame.FULLSCREEN)
            else:
                self._screen = pygame.display.set_mode(WINDOW_SIZE)
                self._full_screen = not self._full_screen

        elif event.key == locals.K_h:
            print(HELP_CONTENT)
        elif event.key == locals.K_SPACE:
            pygame.image.save(self._screen, 'screenshots/screenshot_%s.png' % str(datetime.now()))

        elif event.key == pygame.K_1:
            self._snake.eat()
        elif event.key == pygame.K_2:
            # food_dispatcher.remove_food()
            self._foodDispatcher.place_food()

    def _handle_player_action(self, event):
        if event.key == pygame.K_LEFT and self._snake.get_move_direction() != 'right':
            print("left")
            self._snake.update_move_direction('left')
        elif event.key == pygame.K_RIGHT and self._snake.get_move_direction() != 'left':
            print("right")
            self._snake.update_move_direction('right')
        elif event.key == pygame.K_UP and self._snake.get_move_direction() != 'down':
            print("up")
            self._snake.update_move_direction('up')
        elif event.key == pygame.K_DOWN and self._snake.get_move_direction() != 'up':
            print("down")
            self._snake.update_move_direction('down')

    def run_game(self):
        while not self._quit:
            #self._clock.tick(FPS)
            self._clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == locals.MOUSEBUTTONDOWN:
                    print(pygame.mouse.get_pos())
                elif event.type == locals.KEYDOWN:
                    self._handle_game_interactions(event)

                    if self._game_mode == 'player':
                        self._handle_player_action(event)

            if self._game_mode == 'ai':
                self._ai.think()

            self._update_snake()

            if self._is_gameover():
                self._quit = self._game_over_menu.run()
                if not self._quit:
                    del (self._snake)
                    self._snake = Snake(WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2, BLOCKSIZE)
                    self._gameField = GameField(self._snake)
                    self._foodDispatcher = FoodDispatcher(self._screen, (BORDER_SIZE, BORDER_SIZE),
                                                    (WINDOW_SIZE[0] - BORDER_SIZE, WINDOW_SIZE[1] - BORDER_SIZE),
                                                          self._gameField)
                    self._ai = AI(self._snake, self._foodDispatcher, self._gameField)
            else:
                self._check_eating()
            pygame.display.update()
