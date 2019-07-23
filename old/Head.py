import pygame

from old.Settings import SNAKE_HEAD_IMG


class Head(pygame.sprite.Sprite):
    def __init__(self, pos_x=0, pos_y=0):
        super(Head, self).__init__()

        self.img = pygame.image.load(SNAKE_HEAD_IMG)

        self._pos_x = pos_x
        self._pos_y = pos_y

    def update_x_position(self, pos):
        self._pos_x = pos

    def update_y_position(self, pos):
        self._pos_y = pos

    def get_pos_x(self):
        return self._pos_x

    def get_pos_y(self):
        return self._pos_y

    def get_position(self):
        return self._pos_x, self._pos_y

    def draw(self, screen, direction="right"):
        angle = 0
        if direction == "left":
            angle = 90
        elif direction == "up":
            angle = 0
        elif direction == "down":
            angle = 180
        elif direction == "right":
            angle = 270

        rotated_img = pygame.transform.rotate(self.img, angle)
        screen.blit(rotated_img, (self._pos_x, self._pos_y))
