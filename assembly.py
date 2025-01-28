from pygame.event import Event
from objects import *


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
        self.shrink = AnimatedText(
            self.surface,
            (50, 100),
            30,
            (255, 255, 255),
        )
        self.light = AnimatedText(
            self.surface,
            (50, 150),
            30,
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
        elif e.type == MOUSEWHEEL:
            val = e.dict["y"]
            if key.get_pressed()[K_LCTRL]:
                Mutable.SHRINK += val * Mutable.SHRINK_SPEED
            else:
                Mutable.LIGHT_RADIUS += val * Mutable.LIGHT_RADIUS_SPEED

    def update(self):
        self.board.update()
        self.clock.tick(FPS)

    def draw(self):
        self.surface.draw()
        self.board.draw()
        self.fps.text = "FPS: %i" % self.clock.get_fps()
        self.shrink.text = "Shrink: %.3f" % Mutable.SHRINK
        self.light.text = "Light: %.3f" % Mutable.LIGHT_RADIUS
        self.fps.draw()
        self.shrink.draw()
        self.light.draw()

    def exit(self):
        quit()
        exit()
