from pygame.event import Event
from objects import *


class GameAssembly:
    def __init__(self):
        init()
        self.surface = Screen()
        self.clock = time.Clock()
        self.board = Board(self.surface)
        self.texts = Values(self.surface)

    def emit(self, e: Event):
        if e.type == QUIT:
            self.exit()
        elif e.type == KEYDOWN:
            if e.dict["key"] == K_ESCAPE:
                self.exit()
            elif e.dict["key"] == K_F11:
                self.surface.switchFull()
        elif e.type == MOUSEWHEEL:
            val = e.dict["y"]
            if key.get_pressed()[K_LCTRL]:
                Mutable.SHRINK += val * Mutable.SHRINK_SPEED
            else:
                Mutable.LIGHT_RADIUS += val * Mutable.LIGHT_RADIUS_SPEED

    def update(self):
        self.board.update()
        self.texts.update(self.clock.get_fps())
        self.clock.tick(FPS)

    def draw(self):
        self.surface.draw()
        self.texts.draw()
        self.board.draw()

    def exit(self):
        quit()
        exit()
