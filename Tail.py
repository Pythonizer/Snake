import pygame


class Tail(list):
    def __init__(self, color, segment_width, segment_height):
        super(Tail, self).__init__()

        self._color = color
        self._width = segment_width
        self._height = segment_height

        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(color)

    def add_tail_segment(self, pos_x, pos_y):
        rect = self.image.get_rect()
        rect[0] = pos_x
        rect[1] = pos_y
        self.append(rect)

    def draw(self, screen):
        for t in self:
            pygame.draw.rect(screen, self._color, t)
