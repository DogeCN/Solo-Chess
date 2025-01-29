from pygame import *


def drawGradient(surface, size, tc, bc):
    for y in range(size[1]):
        ratio = y / size[1]
        r = int(tc[0] * (1 - ratio) + bc[0] * ratio)
        g = int(tc[1] * (1 - ratio) + bc[1] * ratio)
        b = int(tc[2] * (1 - ratio) + bc[2] * ratio)
        draw.line(surface, (r, g, b), (0, y), (size[0], y))
