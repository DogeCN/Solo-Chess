from pygame import *
from constants import *


class Screen(Surface):
    def __init__(self):
        SIZE = (WIDTH, HEIGHT)
        super().__init__(SIZE)
        self.screen = display.set_mode(SIZE)
        display.set_caption(CAPTION)

    def draw(self):
        self.screen.blit(self, (0, 0))
        self.fill(COLOR)
        display.flip()


class BCollide(Rect):
    def __init__(self):
        super().__init__(0, 0, 0, 0)
        self.center = B_LEFTTOP
        self.size = B_STRETCH

    def collidepoint(self, pos):
        return super().collidepoint(pos)


class Trapezoid(Rect):
    def __init__(self, surface):
        self.points = [(0, 0)] * 4
        self.surface = surface

    @property
    def topLeft(self):
        return self.points[0]

    @topLeft.setter
    def topLeft(self, value):
        self.points[0] = value

    @property
    def topRight(self):
        return self.points[1]

    @topRight.setter
    def topRight(self, value):
        self.points[1] = value

    @property
    def bottomRight(self):
        return self.points[2]

    @bottomRight.setter
    def bottomRight(self, value):
        self.points[2] = value

    @property
    def bottomLeft(self):
        return self.points[3]

    @bottomLeft.setter
    def bottomLeft(self, value):
        self.points[3] = value

    def draw(self, color):
        return draw.polygon(self.surface, color, self.points)
