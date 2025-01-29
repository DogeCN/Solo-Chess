from pygame import *
from values import *


class Screen(Surface):
    def __init__(self):
        super().__init__(SIZE)
        self.screen = display.set_mode(SIZE)
        display.set_caption(CAPTION)

    def drawGradient(self, top, bottom):
        for y in range(SIZE[1]):
            ratio = y / SIZE[1]
            r = int(top[0] * (1 - ratio) + bottom[0] * ratio)
            g = int(top[1] * (1 - ratio) + bottom[1] * ratio)
            b = int(top[2] * (1 - ratio) + bottom[2] * ratio)
            draw.line(self, (r, g, b), (0, y), (SIZE[0], y))

    def switchFull(self):
        display.toggle_fullscreen()

    def draw(self):
        display.flip()
        self.screen.blit(self, (0, 0))
        self.drawGradient(BLACK, GREY)


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

    def __init__(self, surface: Surface, pos=(0, 0), mode=VERTICAL, space=5):
        super().__init__(SIZE, SRCALPHA)
        self.surface = surface
        self.pos = pos
        self.mode = mode
        self.space = space

    def calcPos(self):
        size = self.get_bounding_rect().size
        pos = mouse.get_pos()
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
        shrink = Mutable.SHRINK * (
            distance / ((CENTER[0] ** 2 + CENTER[1] ** 2) ** 0.5)
        )
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
        intensity = max(0, min(1, 1 - distance / Mutable.LIGHT_RADIUS))
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
