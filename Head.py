import pygame
from Settings import SNAKE_HEAD_IMG


class Head(pygame.sprite.Sprite):
    def __init__(self, color, width, height, pos_x=0, pos_y=0):
        super(Head, self).__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        #self.image = pygame.Surface([width, height])
        #self.image.fill(color)

        self.img = pygame.image.load(SNAKE_HEAD_IMG)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        #self.rect = self.image.get_rect()
        #self.rect[0] = pos_x
        #self.rect[1] = pos_y
        self._pox_x = pos_x
        self._pox_y = pos_y

    def update_x_position(self, pos):
        #self.rect[0] = pos
        self._pox_x = pos

    def update_y_position(self, pos):
        #self.rect[1] = pos
        self._pox_y = pos

    def get_pos_x(self):
        #return self.rect[0]
        return self._pox_x

    def get_pos_y(self):
        #return self.rect[1]
        return self._pox_y

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
        screen.blit(rotated_img, (self._pox_x, self._pox_y))
