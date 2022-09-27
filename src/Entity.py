from typing_extensions import Self

from src.Point import Point
from src.Polygon import Polygon


class Entity(Polygon):
    def __init__(self, *v: Point):
        super().__init__(*v)
        self.min, self.max = self.getLimits()

    def collision(self, bbox: Self) -> bool:
        return self.min.x <= bbox.max.x and self.max.x >= bbox.min.x and (
            self.min.y <= bbox.max.y and self.max.y >= bbox.min.y)
