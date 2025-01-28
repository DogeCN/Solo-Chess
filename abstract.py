from pygame import *
from constants import *


class Screen(Surface):
    def __init__(self):
        super().__init__(SIZE)
        self.screen = display.set_mode(SIZE)
        display.set_caption(CAPTION)

    def drawGradient(self, color1, color2):
        for y in range(SIZE[1]):
            ratio = y / SIZE[1]
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line(self, (r, g, b), (0, y), (SIZE[0], y))

    def switchFull(self):
        display.toggle_fullscreen()

    def draw(self):
        self.screen.blit(self, (0, 0))
        self.drawGradient(BLACK, GREY)
        display.flip()


class AnimatedText(font.Font):
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
        size = render.get_size()
        pos = mouse.get_pos()
        delta = (
            min(WIDTH / (pos[0] + self.pos[0]), WIDTH / size[0]) * 2,
            min(HEIGHT / (pos[1] + self.pos[0]), HEIGHT / size[1]) * 2,
        )
        self.surface.blit(render, (self.pos[0] + delta[0], self.pos[1] + delta[1]))


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
    def __init__(self, surface, topleft, size):
        super().__init__(surface)
        self.topleft = topleft
        self.size = size
        self.recover()

    def recover(self):
        self.topLeft = self.topleft
        self.topRight = self.topright
        self.bottomRight = self.bottomright
        self.bottomLeft = self.bottomleft

    def adjust_point(self, point, pos):
        dx = point[0] - pos[0]
        dy = point[1] - pos[1]
        distance = ((dx**2) + (dy**2)) ** 0.5
        shrink = SHRINK * (distance / ((CENTER[0] ** 2 + CENTER[1] ** 2) ** 0.5))
        x = point[0] - dx * shrink
        y = point[1] - dy * shrink
        return (x, y)

    def resize(self, pos):
        self.topLeft = self.adjust_point(self.topLeft, pos)
        self.topRight = self.adjust_point(self.topRight, pos)
        self.bottomRight = self.adjust_point(self.bottomRight, pos)
        self.bottomLeft = self.adjust_point(self.bottomLeft, pos)

    def update(self):
        self.recover()
        pos = mouse.get_pos()
        self.resize(pos)

    def calcIntensity(self, pos, point):
        dx = pos[0] - point[0]
        dy = pos[1] - point[1]
        distance = (dx**2 + dy**2) ** 0.5
        intensity = max(0, min(1, 1 - distance / LIGHT_RADIUS))
        return intensity

    def light(self, color):
        pos = mouse.get_pos()
        intensity = sum(self.calcIntensity(pos, point) for point in self.points) / 4
        return (
            min(255, int(color[0] * intensity)),
            min(255, int(color[1] * intensity)),
            min(255, int(color[2] * intensity)),
        )

    def draw(self, color):
        if LIGHT:
            color = self.light(color)
        return super().draw(color)
