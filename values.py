WIDTH = 1156
HEIGHT = 650
SIZE = WIDTH, HEIGHT
CENTER = WIDTH // 2, HEIGHT // 2
CAPTION = "Solo Chess"
FPS = 60

C_SIZE = 65, 65
C_GROUP = 3, 3
C_INSIDE = 3, 3
COLUMN = C_GROUP[0] * C_INSIDE[0]
ROW = C_GROUP[1] * C_INSIDE[1]
B_SIZE = C_SIZE[0] * COLUMN, C_SIZE[1] * ROW
B_TOPLEFT = [(SIZE[i] - B_SIZE[i]) // 2 for i in range(2)]

LINE_WIDTH = 1
BORDER_WIDTH = 3

DEFAULT_SIZE = 36
HORIZONTAL = 0
VERTICAL = 1
MAX_DELTA_RATE = 10

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 50, 50, 50
DEEP_GREY = 20, 20, 20
SILVER = 128, 128, 128
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0
RED = 255, 0, 0
INDEXES = (SILVER, GREEN, BLUE)

OFFSET_RADIUS = 100
BLUR = 5


class Mutable:
    LIGHT = True
    _LIGHT_RADIUS = 1000
    LIGHT_RADIUS_SPEED = 100
    LIGHT_RADIUS_MAX = 10000
    LIGHT_RADIUS_MIN = 100
    _SHRINK = 0.05
    SHRINK_SPEED = 0.05
    SHRINK_MAX = 5
    SHRINK_MIN = 0

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
