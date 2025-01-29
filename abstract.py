from methods import *
from values import *


class Screen(Surface):

    def __init__(self):
        super().__init__(SIZE)
        self.screen = display.set_mode(SIZE)
        display.set_caption(CAPTION)

    def switchFull(self):
        display.toggle_fullscreen()

    def getPos(self):
        pos = list(mouse.get_pos())
        size = self.screen.get_size()
        pos_ = pos[:]
        for i in range(2):
            pos[i] = pos[i] * size[i] // SIZE[i]
        if pos != pos_:
            print(pos, pos_)
        return pos

    def draw(self):
        display.flip()
        self.screen.blit(transform.scale(self, self.screen.get_size()), (0, 0))
        drawGradient(self, SIZE, BLACK, GREY)


class TextRender(font.Font):
    def __init__(
        self,
        size=DEFAULT_SIZE,
        color=WHITE,
        text="",
    ):
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
        pos = self.surface.getPos()
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

    def drawLine(self, start, end, color, width=1):
        draw.line(self.surface, color, start, end, width)

    def drawGrid(self, color):
        self.drawLine(self.topLeft, self.topRight, color)
        self.drawLine(self.topRight, self.bottomRight, color)
        self.drawLine(self.bottomRight, self.bottomLeft, color)
        self.drawLine(self.bottomLeft, self.topLeft, color)

    def draw(self, color):
        return draw.polygon(self.surface, color, self.points)


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
        dx = point[0] - pos[0]
        dy = point[1] - pos[1]
        distance = ((dx**2) + (dy**2)) ** 0.5
        shrink = Mutable.SHRINK * (
            distance / ((CENTER[0] ** 2 + CENTER[1] ** 2) ** 0.5)
        )
        x = point[0] - dx * shrink
        y = point[1] - dy * shrink
        return (x, y)

    def resize(self, pos):
        for i in range(4):
            self.points[i] = self.adjustPoint(self.points[i], pos)

    def update(self):
        self.recover()
        pos = self.surface.getPos()
        self.resize(pos)

    def calcIntensity(self, pos, point):
        dx = pos[0] - point[0]
        dy = pos[1] - point[1]
        distance = (dx**2 + dy**2) ** 0.5
        intensity = max(0, min(1, 1 - distance / Mutable.LIGHT_RADIUS))
        return intensity

    def light(self, color):
        pos = self.surface.getPos()
        intensity = sum(self.calcIntensity(pos, point) for point in self.points) / 4
        return [min(255, int(c * intensity)) for c in color]

    def draw(self, color):
        if LIGHT:
            color = self.light(color)
        return super().draw(color)
