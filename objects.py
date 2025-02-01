from pygame import *
from values import *
from abstract import *


class ChessCell(AnimatedTrapezoid):
    index = 0

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

    def update(self):
        super().update()
        self.color = None
        self.allowed = True

    def draw(self):
        if not self.allowed:
            color = RED
        elif self.index:
            color = INDEXES[self.index]
        elif self.color:
            color = self.color
        else:
            color = INDEXES[0]
        super().draw(color)
        self.drawGrid(GREY)


class ChessGroup:
    def __init__(self, globals: "Globals", surface: Screen, c, r):
        self.globals = globals
        self.col, self.row = c, r
        self.cells = [
            ChessCell(self, surface, c, r)
            for c in range(C_INSIDE[0])
            for r in range(C_INSIDE[1])
        ]

    def isChild(self, cell: ChessCell):
        return cell in self.cells

    def draw(self):
        for cell in self.cells:
            cell.draw()


class Globals:
    matched: ChessGroup = None
    fixed: ChessGroup = None
    current: ChessCell = None
    pressing: ChessCell = None
    player = 1

    def __init__(self, surface: Screen):
        self.surface = surface
        self.groups = [
            ChessGroup(self, surface, c, r)
            for c in range(C_GROUP[0])
            for r in range(C_GROUP[1])
        ]

    def match(self, group: ChessGroup, cell: ChessCell):
        matched = (
            self.current
            and group.col == self.current.col
            and group.row == self.current.row
        )
        if matched:
            self.matched = group
        if self.fixed:
            if matched and cell.allowed or self.fixed is group:
                cell.color = RED

    def set(self, current: ChessCell):
        self.current = current
        if self.getAllowed(current):
            current.allowed = True
            current.color = INDEXES[self.player]
        else:
            current.allowed = False

    def getAllowed(self, current: ChessCell):
        return (
            self.fixed
            and self.fixed.isChild(current)
            and not current.index
            or not current.index
        )

    def click(self, cell: ChessCell):
        cell.index = self.player
        self.player = 3 - self.player

    def press(self):
        pos = self.surface.getPos()
        for cell in self.cells:
            if cell.collidepoint(pos):
                self.pressing = cell

    def release(self):
        pos = self.surface.getPos()
        for cell in self.cells:
            if cell.collidepoint(pos) and self.pressing is cell and cell.allowed:
                self.click(cell)
                self.fixed = self.matched
                break
        else:
            self.pressing = None

    @property
    def cells(self):
        for group in self.groups:
            for cell in group.cells:
                yield cell

    def update(self):
        pos = self.surface.getPos()
        for group in self.groups:
            for cell in group.cells:
                cell.update()
                self.match(group, cell)
                if cell.collidepoint(pos):
                    self.set(cell)

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
