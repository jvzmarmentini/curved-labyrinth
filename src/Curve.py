import random
from collections import deque
from typing import Deque, NamedTuple

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from typing_extensions import Self

from src.Drawer import Drawer
from src.Point import Point
from src.Polygon import Polygon


class Curve(Polygon):
    def __init__(self, vertices):
        super().__init__(vertices=vertices)
        self.lowNeighbours: Deque[NamedTuple[Self, int]] = deque()
        self.upNeighbours: Deque[NamedTuple[Self, int]] = deque()
        self.color = .5, .5, .5

    def __len__(self) -> int:
        return len(self.curvePoints)

    def __str__(self) -> str:
        return f"Curve={id(self)}, OnRails={list(map(str,self.charsOnRails))}"

    def randLowNeighbours(self):
        return random.choice(list(self.lowNeighbours))

    def randUpNeighbours(self):
        return random.choice(list(self.upNeighbours))

    def generate(self) -> None:
        Drawer.drawCoords(self.lerp(0))
        Drawer.drawCoords(self.lerp(1))
        glLineWidth(2)
        glBegin(GL_LINES)
        for t in np.linspace(.0, 1, num=40):
            cur = self.lerp(t)
            if t != .0:
                Drawer.drawLine(prev, cur, *self.color)
            prev = cur
        glEnd()

    def lerp(self, t: float) -> Point:
        controlPointA = self.vertices[0] * (1-t) + self.vertices[1] * t
        controlPointB = self.vertices[1] * (1-t) + self.vertices[2] * t
        return controlPointA * (1-t) + controlPointB * t

    def derivative(self, t: float) -> Point:
        p0, p1, p2 = self.vertices
        return (p1 - p0) * 2 * (1-t) + (p2 - p1) * 2 * t
