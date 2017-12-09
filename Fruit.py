import pygame


class Fruit(pygame.sprite.Sprite):
    def __init__(self, color, width, height, pos_x, pos_y):
        super(Fruit, self).__init__()

        self._color = color
        self._width = width
        self._height = height

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect[0] = pos_x
        self.rect[1] = pos_y

    def update_x_position(self, pos):
        self.rect[0] = pos

    def update_y_position(self, pos):
        self.rect[1] = pos

    def get_pos_x(self):
        return self.rect[0]

    def get_pos_y(self):
        return self.rect[1]

    def get_size(self):
        return self._height
