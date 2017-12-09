import pygame
from pygame import locals

import sys
import subprocess

from GameMenu import GameMenu


class StartMenu(GameMenu):

    TITLE = "START MENU"

    def __init__(self, screen, items):
        super(StartMenu, self).__init__(screen, items)

    def run(self):
        while self.menu_loop:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == locals.KEYDOWN:
                    if event.key == locals.K_q or event.key == locals.K_ESCAPE:
                        sys.exit()
                    elif event.key == locals.K_1:
                        # Start game
                        self.menu_loop = False
                    elif event.key == locals.K_2:
                        # Select something else
                        print 'Settings'
                        pass

            # Redraw the background
            self.screen.fill(self.bg_color)

            self.screen.blit(self._title, [self._title_pos_x, self._title_pos_y])

            for name, label, (width, height), (posx, posy) in self._options:
                self.screen.blit(label, (posx, posy))

            pygame.display.flip()
