from pygame import *


def triangle(x: int, y: int):
    return (x**2 + y**2) ** 0.5


def calcIntensity(pos: tuple[int, int], point: tuple[int, int], radius: int):
    delta = [pos[i] - point[i] for i in range(2)]
    return max(0, min(1, 1 - triangle(*delta) / radius))


def drawGradient(surface, size: tuple[int, int], *colors: tuple[int, int, int]):
    for y in range(size[1]):
        ratio = y / size[1]

        def fade(colors: list[tuple[int, int, int]]):
            before, after = colors
            return int(before * (1 - ratio) + after * ratio)

        draw.line(surface, tuple(map(fade, zip(*colors))), (0, y), (size[0], y))
