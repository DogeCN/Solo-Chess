class Distance:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def delta_x(self) -> int:
        return self.x2 - self.x1

    def delta_y(self) -> int:
        return self.y2 - self.y1

    def distance(self) -> float:
        return (self.delta_x() ** 2 + self.delta_y() ** 2) ** 0.5
