from pygame import *
from values import *
from abstract import *


class ChessCell(AnimatedTrapezoid):
    clicked = False
    color = SILVER

    def __init__(self, group: "ChessGroup", surface: Screen, c, r):
        self.group = group
        self.col, self.row = c, r
        cx = (group.col * C_INSIDE[0] + c) * C_SIZE[1]
        cy = (group.row * C_INSIDE[1] + r) * C_SIZE[0]
        super().__init__(surface, (B_TOPLEFT[0] + cx, B_TOPLEFT[1] + cy), C_SIZE)

    def drawGrid(self, color):
        if Mutable.LIGHT:
            color = self.light(color)
        super().drawGrid(color)
        if self.group.col and not self.col:
            self.drawLine(self.topLeft, self.bottomLeft, color, BORDER_WIDTH)
        if self.group.row and not self.row:
            self.drawLine(self.topLeft, self.topRight, color, BORDER_WIDTH)

    def draw(self):
        super().draw(self.light(self.color) if Mutable.LIGHT else self.color)
        self.drawGrid(GREY)


class ChessGroup:
    matched = False

    def __init__(self, globals: "Globals", surface: Screen, c, r):
        self.globals = globals
        self.col, self.row = c, r
        self.cells = [
            ChessCell(self, surface, c, r)
            for c in range(C_INSIDE[0])
            for r in range(C_INSIDE[1])
        ]

    def calcColor(self, cell: ChessCell, pos):
        color = SILVER
        if self.matched:
            color = RED_ALPHA
        if cell.collidepoint(pos):
            color = YELLOW_ALPHA
            self.globals.match(cell.col, cell.row)
        elif cell.clicked:
            color = GREEN
        return color

    def update(self, pressed: list, pos):
        for cell in self.cells:
            cell.update()
            if True in pressed and cell.collidepoint(pos):
                cell.clicked = not pressed.index(True)
            cell.color = self.calcColor(cell, pos)

    def draw(self):
        for cell in self.cells:
            cell.draw()


class Globals:
    def __init__(self, surface: Screen):
        self.surface = surface
        self.groups = [
            ChessGroup(self, surface, c, r)
            for c in range(C_GROUP[0])
            for r in range(C_GROUP[1])
        ]

    def match(self, c: int, r: int):
        for group in self.groups:
            group.matched = group.col == c and group.row == r

    def update(self):
        pressed = mouse.get_pressed()
        pos = self.surface.getPos()
        for group in self.groups:
            group.update(pressed, pos)

    def draw(self):
        for group in self.groups:
            group.draw()


class Board(AnimatedTrapezoid):
    def __init__(self, surface: Screen):
        super().__init__(surface, B_TOPLEFT, B_SIZE)
        self.globals = Globals(surface)

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
        self.globals.update()

    def draw(self):
        super().draw(DEEP_GREY)
        self.globals.draw()


class Values(AnimatedTextGroup):
    def __init__(self, surface, pos=(0, 0), mode=VERTICAL, space=5):
        super().__init__(surface, pos, mode, space)
        self.fps = TextRender(36)
        self.shrink = TextRender(30)
        self.light = TextRender(30)

    def update(self, fps):
        self.fps.text = "FPS: %i" % fps
        self.shrink.text = "Shrink: %.2f" % Mutable.SHRINK
        light = round(Mutable.LIGHT_RADIUS, 2) if Mutable.LIGHT else None
        self.light.text = f"Light: {light}"

    def draw(self):
        super().draw(self.fps, self.shrink, self.light)
