from pygame import *
from constants import *
from abstract import *


class ChessCell(AnimatedTrapezoid):
    def __init__(self, surface: Surface, c, r):
        super().__init__(
            surface,
            (B_TOPLEFT[0] + c * C_SIZE[1], B_TOPLEFT[1] + r * C_SIZE[0]),
            C_SIZE,
        )
        self.clicked = False

    def update(self):
        super().update()
        pressed = mouse.get_pressed()
        if True in pressed and self.collidepoint(mouse.get_pos()):
            self.clicked = not pressed.index(True)

    def draw(self):
        pos = mouse.get_pos()
        if self.collidepoint(pos):
            super().draw(YELLOW)
        elif self.clicked:
            super().draw(GREEN)
        else:
            super().draw(SILVER)


class Board(AnimatedTrapezoid):
    def __init__(self, surface):
        super().__init__(surface, B_TOPLEFT, B_SIZE)
        self.frames = [
            [ChessCell(surface, c, r) for c in range(COLUMN)] for r in range(ROW)
        ]

    def update(self):
        super().update()
        for row in self.frames:
            for frame in row:
                frame.update()

    def draw(self):
        super().draw(WHITE)
        for row in self.frames:
            for frame in row:
                frame.draw()
