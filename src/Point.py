import math
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
        return Point(*[a + b for a, b in zip(self, other)])

    def __sub__(self, other: Self) -> Self:
        return Point(*[abs(a) - abs(b) for a, b in zip(self, other)])

    def __mul__(self, other: float) -> Self:
        return Point(*[a * other for a in self])

    def rotateZ(self, angulo: float) -> Self:
        anguloRad = angulo * 3.14159265359/180.0
        xr = self.x*math.cos(anguloRad) - self.y*math.sin(anguloRad)
        yr = self.x*math.sin(anguloRad) + self.y*math.cos(anguloRad)

        return Point(xr, yr, self.z)

    def rotateY(self, angulo: float) -> None:
        anguloRad = angulo * 3.14159265359/180.0
        xr = self.x*math.cos(anguloRad) + self.z*math.sin(anguloRad)
        zr = -self.x*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.x = xr
        self.z = zr

    def rotateX(self, angulo: float) -> None:
        anguloRad = angulo * 3.14159265359/180.0
        yr = self.y*math.cos(anguloRad) - self.z*math.sin(anguloRad)
        zr = self.y*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.y = yr
        self.z = zr
