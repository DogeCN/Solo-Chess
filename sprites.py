from pygame import *
from constants import *
from abstract import *


class Board(AnimatedTrapezoid):
    def __init__(self, surface):
        super().__init__(surface)

    def update(self):
        return super().update()

    def draw(self):
        super().draw(WHITE)
        pass
