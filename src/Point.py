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
        self.x = xr
        self.y = yr

        return self

    def rotacionaY(self, angulo: float) -> None:
        anguloRad = angulo * 3.14159265359/180.0
        xr = self.x*math.cos(anguloRad) + self.z*math.sin(anguloRad)
        zr = -self.x*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.x = xr
        self.z = zr

    def rotacionaX(self, angulo: float) -> None:
        anguloRad = angulo * 3.14159265359/180.0
        yr = self.y*math.cos(anguloRad) - self.z*math.sin(anguloRad)
        zr = self.y*math.sin(anguloRad) + self.z*math.cos(anguloRad)
        self.y = yr
        self.z = zr