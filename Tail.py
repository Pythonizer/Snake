import pygame


class Tail(pygame.sprite.Sprite):
    def __init__(self, color, width, height, pos_x, pos_y):
        super(Tail, self).__init__()

        self._color = color
        self._width = width
        self._height = height

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
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
