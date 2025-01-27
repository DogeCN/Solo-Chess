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


class ChessPiece(sprite.Sprite):
    def __init__(self, surface: Surface, c, r):
        super().__init__()
        self.clicked = False
        self.surface = surface
        self.frame = ChessCell(surface, c, r)
        self.rect = self.frame.copy()

    def update(self):
        self.frame.update()
        pressed = mouse.get_pressed()
        if True in pressed and self.rect.collidepoint(mouse.get_pos()):
            self.clicked = not pressed.index(True)

    def draw(self):
        pos = mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.frame.draw(YELLOW)
        elif self.clicked:
            self.frame.draw(GREEN)
        else:
            self.frame.draw(GRAY)


class Board(AnimatedTrapezoid):
    def __init__(self, surface):
        super().__init__(surface, B_TOPLEFT, B_SIZE)
        self.frames = [
            [ChessPiece(surface, c, r) for c in range(COLUMN)] for r in range(ROW)
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
