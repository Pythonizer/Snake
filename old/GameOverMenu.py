import sys

import pygame
from pygame import locals

from old.GameMenu import GameMenu


class GameOverMenu(GameMenu):

    TITLE = "GAME OVER"

    def __init__(self, screen, items, font_color=(255, 0, 0)):
        super(GameOverMenu, self).__init__(screen, items, font_color=font_color)

    def run(self):
        quit = True
        self.menu_loop = True
        while self.menu_loop:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == locals.KEYDOWN:
                    if event.key == locals.K_q or event.key == locals.K_ESCAPE:
                        sys.exit()
                    elif event.key == locals.K_1:
                        self.menu_loop = False
                        quit = False
                    elif event.key == locals.K_2:
                        quit = False
                        self.menu_loop = False
                    elif event.key == locals.K_3:
                        quit = True
                        self.menu_loop = False

            # Redraw the background
            #self.screen.fill(self.bg_color)

            self.screen.blit(self._title, [self._title_pos_x, self._title_pos_y])

            for name, label, (width, height), (posx, posy) in self._options:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()
        print("Quit: %s" % quit)
        return quit
