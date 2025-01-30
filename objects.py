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
        self.col, self.row = c, r
        self.color = SILVER
        self.clicked = False

    def drawGrid(self, color):
        super().drawGrid(color)
        if self.col and not self.col % C_INSIDE[0]:
            self.drawLine(self.topLeft, self.bottomLeft, color, BORDER_WIDTH)
        if self.row and not self.row % C_INSIDE[1]:
            self.drawLine(self.topLeft, self.topRight, color, BORDER_WIDTH)

    def draw(self):
        super().draw(self.color)
        self.drawGrid(GREY)


class ChessGroup:
    def __init__(self, surface: Screen, c, r):
        self.col, self.row = c, r
        self.cells = [
            ChessCell(surface, c * C_INSIDE[0] + cc, r * C_INSIDE[1] + cr)
            for cc in range(C_INSIDE[0])
            for cr in range(C_INSIDE[1])
        ]

    def update(self, pressed: list, pos):
        for cell in self.cells:
            cell.update()
            if True in pressed and cell.collidepoint(pos):
                cell.clicked = not pressed.index(True)
            cell.color = (
                YELLOW if cell.collidepoint(pos) else GREEN if cell.clicked else SILVER
            )

    def draw(self):
        for cell in self.cells:
            cell.draw()


class Board(AnimatedTrapezoid):
    def __init__(self, surface: Screen):
        super().__init__(surface, B_TOPLEFT, B_SIZE)
        self.groups = [
            ChessGroup(surface, c, r)
            for c in range(C_GROUP[0])
            for r in range(C_GROUP[1])
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
        pressed = mouse.get_pressed()
        pos = self.surface.getPos()
        for group in self.groups:
            group.update(pressed, pos)

    def draw(self):
        super().draw(DEEP_GREY)
        for group in self.groups:
            group.draw()


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
