import pygame


class Head(pygame.sprite.Sprite):
    def __init__(self, color, width, height, pos_x=0, pos_y=0):
        super(Head, self).__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
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

    def draw(self):
        pygame.draw.rect()


