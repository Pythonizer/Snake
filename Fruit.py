import pygame
from Settings import APPLE_IMG, BLOCKSIZE


class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super(Fruit, self).__init__()

        #self.image = pygame.Surface([width, height])
        #self.image.fill(color)

        self.img = pygame.image.load(APPLE_IMG)

        #self.rect = self.image.get_rect()
        self._pos_x = pos_x
        self._pos_y = pos_y
        #self.rect[0] = pos_x
        #self.rect[1] = pos_y

    def draw(self, screen):
        screen.blit(self.img, (self._pos_x, self._pos_y))
        #pygame.draw.rect(screen, self._color, self.rect)

    def update_x_position(self, pos):
        self._pos_x = pos
        #self.rect[0] = pos

    def update_y_position(self, pos):
        #self.rect[1] = pos
        self._pos_y = pos

    def get_pos_x(self):
        #return self.rect[0]
        return self._pos_x

    def get_pos_y(self):
        #return self.rect[1]
        return self._pos_y

    def get_size(self):
        return BLOCKSIZE
