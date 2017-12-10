import pygame
from pygame import locals

import sys
import subprocess
from Settings import FONT_1


class GameMenu(object):

    FPS = 50
    TITLE = "GAME MENU"

    def __init__(self, screen, items, bg_color=(0, 0, 0), font_size=30,
                 font_color=(255, 255, 255)):

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.menu_loop = None

        self.bg_color = bg_color

        self.clock = pygame.time.Clock()
        #self.font = pygame.font.SysFont(None, font_size)
        self.font_color = font_color

        # Prepare title
        print self.TITLE
        self._title_font = pygame.font.Font(FONT_1, font_size*2)
        self._title_color = self.font_color
        self._title = self._title_font.render(self.TITLE, 1, self._title_color)
        self._title_pos_x = (self.scr_width/2) - (self._title.get_rect().width/2)
        self._title_pos_y = self.scr_height/4

        # Prepare menu options
        self.font = pygame.font.Font(FONT_1, font_size)
        self._chosen_option = None
        self._options = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, self.font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            posx = (self.scr_width / 2) - (width / 2)
            # t_h: total height of text block
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)

            self._options.append([item, label, (width, height), (posx, posy)])

    # def _prepare_menu_points(self, items):
    #     menu_points = []
    #     nr = 1
    #     for index, item in enumerate(items):
    #         label = self.font.render(str(nr) + '. ' + item, 1, self.font_color)
    #         nr += 1
    #
    #         width = label.get_rect().width
    #         height = label.get_rect().height
    #
    #         posx = (self.scr_width / 2) - (width / 2)
    #         # t_h: total height of text block
    #         t_h = len(items) * height
    #         posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
    #
    #         menu_points.append([item, label, (width, height), (posx, posy)])
    #     return menu_points

    # def chose_item(self):
    #     # Just demo case
    #     self._chosen_item = True
    #     return
    #
    #     items = subprocess.check_output(['ls', '<items>']).split()
    #
    #     menu_points = self._prepare_menu_points(items)
    #
    #     choosing_item = True
    #     while choosing_item:
    #         self.clock.tick(50)
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 sys.exit()
    #             elif event.type == locals.KEYDOWN:
    #                 if event.key == locals.K_q or event.key == locals.K_ESCAPE:
    #                     sys.exit()
    #                     # 49 ^= 1
    #                 elif 49 <= event.key < (49 + len(menu_points)):
    #                     print event.key
    #                     key_index = event.key - 49
    #                     self._chosen_item = items[key_index]
    #                     choosing_item = False
    #
    #                     # Redraw the background
    #         self.screen.fill(self.bg_color)
    #
    #         for name, label, (width, height), (posx, posy) in menu_points:
    #             self.screen.blit(label, (posx, posy))
    #
    #         pygame.display.flip()
