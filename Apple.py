import pygame

from Fruit import Fruit
import Colors
from Settings import BLOCKSIZE


class Apple(Fruit):
    def __init__(self, pos_x, pos_y, size=BLOCKSIZE, color=Colors.APPLE_RED):
        super(Apple, self).__init__(color, size, size, pos_x, pos_y)
