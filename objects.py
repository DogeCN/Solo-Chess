from pygame import *
from values import *
from abstract import *


class ChessCell(AnimatedTrapezoid):
    color = SILVER
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
        self.drawLine(
            self.topLeft,
            self.bottomLeft,
            color,
            BORDER_WIDTH if self.group.col and not self.col else LINE_WIDTH,
        )
        self.drawLine(
            self.topLeft,
            self.topRight,
            color,
            BORDER_WIDTH if self.group.row and not self.row else LINE_WIDTH,
        )
        self.drawLine(self.topRight, self.bottomRight, color)
        self.drawLine(self.bottomRight, self.bottomLeft, color)

    def draw(self):
        super().draw(self.color)
        self.drawGrid(GREY)


class ChessGroup:
    index = 0

    def __init__(self, globals: "Globals", surface: Screen, c, r):
        self.globals = globals
        self.col, self.row = c, r
        self.cells = [
            ChessCell(self, surface, c, r)
            for c in range(C_INSIDE[0])
            for r in range(C_INSIDE[1])
        ]

    def has(self, cell: ChessCell):
        return cell in self.cells

    def isMatched(self, cell: ChessCell):
        return cell.col == self.col and cell.row == self.row

    def setIndex(self, index):
        self.index = index
        for cell in self.cells:
            cell.index = index

    def check(self):
        cells: list[list[ChessCell]] = [[] for _ in range(3)]
        for cell in self.cells:
            if cell.index:
                cells[cell.index - 1].append(cell)
        for i in range(2):
            p = cells[i]
            if len(p) >= CONST:
                probs = [[] for _ in range(4)]
                for cell in p:
                    probs[0].append(cell.col)
                    probs[1].append(cell.row)
                    probs[2].append(cell.col + cell.row)
                    probs[3].append(cell.col - cell.row)
                for prob in probs:
                    for p in set(prob):
                        if prob.count(p) >= CONST:
                            self.setIndex(i + 1)
                            return True
        if sum(map(len, cells)) == len(self.cells):
            self.setIndex(3)

    def draw(self):
        for cell in self.cells:
            cell.draw()


class Globals:
    matched: ChessGroup = None
    fixed: ChessGroup = None
    current: ChessCell = None
    pressing: ChessCell = None
    player = 1
    index = 0

    def __init__(self, surface: Screen):
        self.surface = surface
        self.groups = [
            ChessGroup(self, surface, c, r)
            for c in range(C_GROUP[0])
            for r in range(C_GROUP[1])
        ]

    def setIndex(self, index):
        self.index = index
        for group in self.groups:
            group.setIndex(index)

    def reset(self):
        self.setIndex(0)
        self.player = 1
        self.fixed = None

    def check(self):
        res = False
        groups: list[list[ChessGroup]] = [[] for _ in range(3)]
        for group in self.groups:
            if group.check() and not group.index:
                res = True
            if group.index:
                groups[group.index - 1].append(group)
        for i in range(2):
            p = groups[i]
            if len(p) >= CONST:
                probs = [[] for _ in range(4)]
                for group in p:
                    probs[0].append(group.row)
                    probs[1].append(group.col)
                    probs[2].append(group.col + group.row)
                    probs[3].append(group.col - group.row)
                for prob in probs:
                    for p in set(prob):
                        if prob.count(p) >= CONST:
                            self.setIndex(i + 1)
                            return True
        if sum(map(len, groups)) == len(self.groups):
            self.setIndex(3)
        return res

    def press(self):
        if self.current and self.allow(self.current):
            self.pressing = self.current
        elif self.index:
            self.reset()

    def release(self):
        current = self.current
        if self.pressing is current is not None:
            current.index = self.player
            self.player = 3 - self.player
            self.fixed = None if self.check() or self.matched.index else self.matched
        self.pressing = None

    def allow(self, cell: ChessCell):
        if self.fixed:
            return self.fixed.has(cell) and not cell.index
        return not cell.index

    def color(self):
        for group in self.groups:
            for cell in group.cells:
                color = SILVER
                oncur = self.current is cell
                if self.matched and self.matched.has(cell):
                    color = YELLOW
                elif self.fixed and self.fixed.has(cell):
                    color = RED
                if cell.index:
                    color = INDEXES[cell.index]
                    if oncur:
                        color = RED
                else:
                    if oncur:
                        if self.allow(cell):
                            color = INDEXES[self.player]
                        else:
                            color = RED
                cell.color = color

    def update(self):
        self.matched = self.current = None
        pos = self.surface.getPos()
        for group in self.groups:
            for cell in group.cells:
                cell.update()
                if cell.collidepoint(pos):
                    self.current = cell
        for group in self.groups:
            if (
                self.current
                and self.allow(self.current)
                and group.isMatched(self.current)
            ):
                self.matched = group
        self.color()

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
