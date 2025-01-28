WIDTH = 1200
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)
CENTER = (WIDTH // 2, HEIGHT // 2)
CAPTION = "Solo Chess"
FPS = 60

B_TOPLEFT = (350, 50)
B_SIZE = (500, 500)
C_SIZE = (50, 50)
COLUMN = B_SIZE[0] // C_SIZE[0]
ROW = B_SIZE[1] // C_SIZE[1]

DEFAULT_SIZE = 36

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (50, 50, 50)
SILVER = (128, 128, 128)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

LIGHT = True


class Mutable:
    _LIGHT_RADIUS = 1000
    LIGHT_RADIUS_SPEED = 100
    LIGHT_RADIUS_MAX = 10000
    LIGHT_RADIUS_MIN = 100
    _SHRINK = 0.05
    SHRINK_SPEED = 0.05
    SHRINK_MAX = 5
    SHRINK_MIN = 0.001

    @property
    def SHRINK(self):
        return self._SHRINK

    @SHRINK.setter
    def SHRINK(self, value):
        self._SHRINK = max(self.SHRINK_MIN, min(self.SHRINK_MAX, value))

    @property
    def LIGHT_RADIUS(self):
        return self._LIGHT_RADIUS

    @LIGHT_RADIUS.setter
    def LIGHT_RADIUS(self, value):
        self._LIGHT_RADIUS = max(
            self.LIGHT_RADIUS_MIN, min(self.LIGHT_RADIUS_MAX, value)
        )


Mutable = Mutable()
