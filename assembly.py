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
        self.fps = AnimatedText(
            self.surface,
            (50, 50),
            36,
            (255, 255, 255),
        )

    def emit(self, e: Event):
        if e.type == QUIT:
            self.exit()
        elif e.type == KEYDOWN:
            if e.dict["key"] == K_ESCAPE:
                self.exit()
            elif e.dict["key"] == K_F11:
                self.surface.switchFull()

    def update(self):
        self.board.update()
        self.clock.tick(FPS)

    def draw(self):
        self.surface.draw()
        self.board.draw()
        self.fps.text = "FPS: %i" % self.clock.get_fps()
        self.fps.draw()

    def exit(self):
        quit()
        exit()
