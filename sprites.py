from pygame import *
from constants import *
from abstract import *
from calculate import *


class Board(Trapezoid):
    def __init__(self, surface):
        super().__init__(surface)
        self.coll = BCollide()
        self.recover()

    def recover(self):
        self.topLeft = self.coll.topleft
        self.topRight = self.coll.topright
        self.bottomRight = self.coll.bottomright
        self.bottomLeft = self.coll.bottomleft

    def resize(self, pos):
        dis = Distance(*self.coll.center, *pos)
        if dis.delta_x() > 0 and dis.delta_y() > 0:
            self.topRight = pos
        elif dis.delta_x() > 0 and dis.delta_y() < 0:
            self.bottomRight = pos
        elif dis.delta_x() < 0 and dis.delta_y() < 0:
            self.bottomLeft = pos
        elif dis.delta_x() < 0 and dis.delta_y() > 0:
            self.topLeft = pos

    def update(self):
        self.recover()
        pos = mouse.get_pos()
        if self.coll.collidepoint(pos):
            self.resize(pos)

    def draw(self):
        super().draw(B_COLOR)
        pass
