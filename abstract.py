from pygame import *
from constants import *


class Screen(Surface):
    def __init__(self):
        super().__init__(SIZE)
        self.screen = display.set_mode(SIZE)
        display.set_caption(CAPTION)

    def toggle_fullscreen(self):
        display.toggle_fullscreen()

    def draw(self):
        self.screen.blit(self, (0, 0))
        self.fill(BLACK)
        display.flip()


class Text(font.Font):
    def __init__(
        self,
        surface: Surface,
        pos=(0, 0),
        size=DEFAULT_SIZE,
        color=WHITE,
        text="",
    ):
        super().__init__(None, size)
        self.surface = surface
        self.color = color
        self.text = text
        self.pos = pos

    def draw(self):
        render = self.render(self.text, True, self.color)
        self.surface.blit(render, self.pos)


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


class AnimatedTrapezoid(Trapezoid):
    def __init__(self, surface):
        super().__init__(surface)
        self.center = B_LEFTTOP
        self.size = B_STRETCH
        self.recover()

    def recover(self):
        self.topLeft = self.topleft
        self.topRight = self.topright
        self.bottomRight = self.bottomright
        self.bottomLeft = self.bottomleft

    def adjust_point(self, point, center, pos):
        dx = point[0] - pos[0]
        dy = point[1] - pos[1]
        distance = ((dx**2) + (dy**2)) ** 0.5
        shrink = SHRINK * (distance / ((center[0] ** 2 + center[1] ** 2) ** 0.5))
        x = point[0] - dx * shrink
        y = point[1] - dy * shrink
        return (x, y)

    def resize(self, pos):
        center_x = (
            self.topLeft[0]
            + self.topRight[0]
            + self.bottomRight[0]
            + self.bottomLeft[0]
        ) / 4
        center_y = (
            self.topLeft[1]
            + self.topRight[1]
            + self.bottomRight[1]
            + self.bottomLeft[1]
        ) / 4
        center = (center_x, center_y)

        self.topLeft = self.adjust_point(self.topLeft, center, pos)
        self.topRight = self.adjust_point(self.topRight, center, pos)
        self.bottomRight = self.adjust_point(self.bottomRight, center, pos)
        self.bottomLeft = self.adjust_point(self.bottomLeft, center, pos)

    def update(self):
        self.recover()
        pos = mouse.get_pos()
        self.resize(pos)
