import pygame

from Fruit import Fruit
import Colors
from Settings import BLOCKSIZE


class Apple(Fruit):
    def __init__(self, pos_x, pos_y):
        super(Apple, self).__init__(pos_x, pos_y)
