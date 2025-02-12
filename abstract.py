from methods import *
from values import *


class Screen(Surface):
    scsize = SIZE
    resized = False
    pos = CENTER

    def __init__(self):
        super().__init__(SIZE, SRCALPHA | DOUBLEBUF)
        self.screen = display.set_mode(SIZE, RESIZABLE)
        display.set_caption(CAPTION)

    def switchFull(self):
        display.toggle_fullscreen()

    def mouseMoved(self):
        pos = mouse.get_pos()
        self.pos = [pos[i] * SIZE[i] // self.scsize[i] for i in range(2)]

    def draw(self):
        if self.resized:
            self.scsize = self.screen.get_size()
            self.resized = False
        self.screen.blit(
            (self if self.scsize == SIZE else transform.smoothscale(self, self.scsize)),
            (0, 0),
        )
        drawGradient(self, SIZE, BLACK, GREY)
        display.flip()


class TextRender(font.Font):
    def __init__(self, size=DEFAULT_SIZE, color=WHITE, text=""):
        super().__init__(None, size)
        self.color = color
        self.text = text

    def render(self):
        return super().render(self.text, True, self.color)


class AnimatedTextGroup(Surface):

    def __init__(self, surface: Screen, pos=(0, 0), mode=VERTICAL, space=5):
        super().__init__(SIZE, SRCALPHA)
        self.surface = surface
        self.pos = pos
        self.mode = mode
        self.space = space

    def calcPos(self):
        size = self.get_bounding_rect().size
        pos = self.surface.pos
        return [
            self.pos[i]
            + min(SIZE[i] / (pos[i] + 1), MAX_DELTA_RATE) * size[i] * Mutable.SHRINK
            for i in range(2)
        ]

    def draw(self, *renders: TextRender):
        pos = [0, 0]
        self.fill((0, 0, 0, 0))
        for t in renders:
            rendered = t.render()
            self.blit(rendered, pos)
            if self.mode == VERTICAL:
                pos[1] += rendered.get_height() + self.space
            elif self.mode == HORIZONTAL:
                pos[0] += rendered.get_width() + self.space
        self.surface.blit(self, self.calcPos())


class Trapezoid(Rect):
    def __init__(self, surface: Screen):
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

    def drawLine(self, start, end, color, width=LINE_WIDTH):
        draw.line(self.surface, color, start, end, width)

    def draw(self, color):
        draw.polygon(self.surface, color, self.points)


class AnimatedTrapezoid(Trapezoid):
    def __init__(self, surface: Screen, topleft, size):
        super().__init__(surface)
        self.topleft = topleft
        self.size = size
        self.recover()

    def recover(self):
        self.topLeft = self.topleft
        self.topRight = self.topright
        self.bottomRight = self.bottomright
        self.bottomLeft = self.bottomleft

    def adjustPoint(self, point, pos):
        delta = [point[i] - pos[i] for i in range(2)]
        distance = triangle(*delta)
        shrink = Mutable.SHRINK * (distance / triangle(*CENTER))
        return [point[i] - delta[i] * shrink for i in range(2)]

    def resize(self, pos):
        for i in range(4):
            self.points[i] = self.adjustPoint(self.points[i], pos)

    def update(self):
        self.recover()
        pos = self.surface.pos
        self.resize(pos)

    def light(self, color):
        pos = self.surface.pos
        intensity = (
            sum(
                calcIntensity(pos, point, Mutable.LIGHT_RADIUS) for point in self.points
            )
            / 4
        )
        return [min(255, int(c * intensity)) for c in color]

    def draw(self, color):
        if Mutable.LIGHT:
            color = self.light(color)
        super().draw(color)
