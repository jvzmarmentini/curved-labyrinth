import math
from typing_extensions import Self


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        return f"x={self.x:.3f} y={self.y:.3f} z={self.z:.3f}"

    def __add__(self, other: Self) -> Self:
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

    def __sub__(self, other: Self) -> Self:
        x = abs(self.x) - abs(other.x)
        y = abs(self.y) - abs(other.y)
        return Point(x, y)

    def __mul__(self, other: float) -> Self:
        x = self.x * other
        y = self.y * other
        return Point(x, y)

    def set(self, x: float, y: float, z: float = 0) -> None:
        self.x = x
        self.y = y
        self.z = z

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

    @staticmethod
    def getMax(a: Self, b: Self) -> Self:
        return Point(max(a.x, b.x),
                     max(a.y, b.y),
                     max(a.z, b.z))

    @staticmethod
    def getMin(a: Self, b: Self) -> Self:
        return Point(min(a.x, b.x),
                     min(a.y, b.y),
                     min(a.z, b.z))
