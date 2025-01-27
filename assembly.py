from pygame import *
from pygame.event import Event
from abstract import Screen
from constants import *
from sprites import *


class GameAssembly:
    def __init__(self):
        init()
        self.surface = Screen()
        self.clock = time.Clock()
        self.board = Board(self.surface)

    def emit(self, e: Event):
        if e.type == QUIT:
            quit()
            exit()
        elif e.type == KEYDOWN:
            if e.dict["key"] == K_ESCAPE:
                quit()

    def update(self):
        self.board.update()

    def draw(self):
        self.surface.draw()
        self.board.draw()
