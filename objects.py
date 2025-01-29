from pygame import *
from values import *
from abstract import *


class ChessCell(AnimatedTrapezoid):
    def __init__(self, surface: Screen, c, r):
        super().__init__(
            surface,
            (B_TOPLEFT[0] + c * C_SIZE[1], B_TOPLEFT[1] + r * C_SIZE[0]),
            C_SIZE,
        )
        self.clicked = False

    def update(self):
        super().update()
        pressed = mouse.get_pressed()
        if True in pressed and self.collidepoint(self.surface.getPos()):
            self.clicked = not pressed.index(True)

    def draw(self):
        super().draw(
            YELLOW
            if self.collidepoint(self.surface.getPos())
            else GREEN if self.clicked else SILVER
        )
        self.drawGrid(GREY)


class Board(AnimatedTrapezoid):
    def __init__(self, surface: Screen):
        super().__init__(surface, B_TOPLEFT, B_SIZE)
        self.frames = [
            [ChessCell(surface, c, r) for c in range(COLUMN)] for r in range(ROW)
        ]

    def offset(self):
        pos = self.surface.getPos()
        for i in range(4):
            point = list(self.points[i])
            for j in range(2):
                point[j] = (
                    point[j]
                    + (pos[j] - CENTER[j])
                    / SIZE[j]
                    * (OFFSET_RADIUS * Mutable.LIGHT_RADIUS * Mutable.SHRINK) ** 0.5
                )
            self.points[i] = tuple(point)

    def update(self):
        super().update()
        self.offset()
        for row in self.frames:
            for frame in row:
                frame.update()

    def draw(self):
        super().draw(DEEP_GREY)
        for row in self.frames:
            for frame in row:
                frame.draw()


class Values(AnimatedTextGroup):
    def __init__(self, surface, pos=(0, 0), mode=VERTICAL, space=5):
        super().__init__(surface, pos, mode, space)
        self.fps = TextRender(36)
        self.shrink = TextRender(30)
        self.light = TextRender(30)

    def update(self, fps):
        self.fps.text = "FPS: %i" % fps
        self.shrink.text = "Shrink: %.2f" % Mutable.SHRINK
        self.light.text = "Light: %2.f" % Mutable.LIGHT_RADIUS

    def draw(self):
        super().draw(self.fps, self.shrink, self.light)
