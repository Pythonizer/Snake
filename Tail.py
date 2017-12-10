import pygame
from Settings import SNAKE_TAIL_IMG, SNAKE_TAIL_BEND_IMG, SNAKE_TAIL_END_IMG


class Tail(list):
    def __init__(self):
        super(Tail, self).__init__()

        self._img = pygame.image.load(SNAKE_TAIL_IMG)
        self._img_bend = pygame.image.load(SNAKE_TAIL_BEND_IMG)
        self._img_end = pygame.image.load(SNAKE_TAIL_END_IMG)

        self._last_direction = None

    def add_tail_segment(self, pos_x, pos_y, direction):
        direction_angle = 0
        if direction == "left":
            direction_angle = 90
        elif direction == "up":
            direction_angle = 0
        elif direction == "down":
            direction_angle = 180
        elif direction == "right":
            direction_angle = 270

        direction_change = False
        bend_angle = 0
        if self._last_direction:
            if self._last_direction != direction:
                # Direction has changed
                direction_change = True
                if self._last_direction == "up":
                    if direction == "left":
                        bend_angle = 270  # -|
                    elif direction == "right":
                        bend_angle = 0  # |-
                elif self._last_direction == "down":
                    if direction == "left":
                        bend_angle = 180  # _|
                    elif direction == "right":
                        bend_angle = 90  # |_
                elif self._last_direction == "left":
                    if direction == "up":
                        bend_angle = 90  # ^-
                    elif direction == "down":
                        bend_angle = 0  # v-
                elif self._last_direction == "right":
                    if direction == "up":
                        bend_angle = 180  # -^
                    elif direction == "down":
                        bend_angle = 270  # -v

        self._last_direction = direction
        self.append([pos_x, pos_y, direction_angle, direction_change, bend_angle])

    def draw(self, screen):
        for t in self[1:]:
            #pygame.draw.rect(screen, self._color, t)
            if t[3]:
                rotated_img = pygame.transform.rotate(self._img_bend, t[4])
                screen.blit(rotated_img, (t[0], t[1]))
            else:
                rotated_img = pygame.transform.rotate(self._img, t[2])
                screen.blit(rotated_img, (t[0], t[1]))
        else:
            if len(self) >= 1:
                rotated_img = pygame.transform.rotate(self._img_end, self[0][2])
                screen.blit(rotated_img, (self[0][0], self[0][1]))
