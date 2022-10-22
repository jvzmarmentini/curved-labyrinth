from math import sqrt
import numpy as np
import typing

from typing_extensions import Self


class Point(typing.NamedTuple):
    x: float = .0
    y: float = .0
    z: float = .0

    def __repr__(self):
        'Return a nicely formatted representation string'
        return f"Point(x={self.x:.2f},y={self.y:.2f},z={self.z:.2f})"

    def __add__(self, other: Self) -> Self:
        return Point(*[x1 + x2 for x1, x2 in zip(self, other)])

    def __sub__(self, other: Self) -> Self:
        return Point(*[x1 - x2 for x1, x2 in zip(self, other)])

    def __mul__(self, other: float) -> Self:
        return Point(*[x1 * other for x1 in self])

    def dot(self, other: Self) -> float:
        return sum([x1 * x2 for x1, x2 in zip(self, other)])

    def normalize(self) -> Self:
        if self.x == self.y == 0:
            return Point()
        d = sqrt(self.x ** 2 + self.y ** 2)
        return Point(self.x / d, self.y / d)

    def translate(self, point: Self) -> Self:
        return Point(*(self + point))

    def scale(self, scale: Self) -> Self:
        return Point(*[x1 * x2 for x1, x2 in zip(self, scale)])

    def rotate(self, angle: float) -> Self:
        """Rotate the point N degrees relative to the Y canonical 3D vector (0, 1, 0)

        Args:
            angle (float): Rotation angle (in degrees)

        Returns:
            Self: A new rotated Point object
        """
        theta = np.deg2rad(angle)
        c, s = np.cos(theta), np.sin(theta)
        rotMatrix = np.array(((c, -s), (s, c)))
        return Point(*(rotMatrix @ self[:2]))
    
    @staticmethod
    def dist(a: Self, b: Self):
        return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
