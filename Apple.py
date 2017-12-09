import pygame

from Fruit import Fruit
import Colors


class Apple(Fruit):
    def __init__(self, pos_x, pos_y, size=30, color=Colors.APPLE_RED):
        super(Apple, self).__init__(color, size, size, pos_x, pos_y)
