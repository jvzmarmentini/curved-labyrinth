import random
from collections import deque
from typing import Deque, NamedTuple

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from typing_extensions import Self

import src.helpers.settings as settings
from src.helpers.Drawer import Drawer
from src.models.Point import Point
from src.models.Polygon import Polygon


class Curve(Polygon):
    _steps = 15
    
    def __init__(self, vertices):
        super().__init__(vertices=vertices)
        self.lowNeighbours: Deque[NamedTuple[Self, int]] = deque()
        self.upNeighbours: Deque[NamedTuple[Self, int]] = deque()
        self.color = .5, .5, .5
        
        self.length = 0

    def __len__(self) -> int:
        return len(self.curvePoints)
    
    @property
    def steps(self):
        return self.__class__._steps
    @steps.setter
    def steps(self, value):
        self.__class__._steps = value

    def randLowNeighbours(self):
        return random.choice(list(self.lowNeighbours))

    def randUpNeighbours(self):
        return random.choice(list(self.upNeighbours))

    def generate(self) -> None:
        if settings._debugger:
            Drawer.drawCoords(self.lerp(0))
            Drawer.drawCoords(self.lerp(1))
        glLineWidth(2)
        glBegin(GL_LINES)
        totalLength = 0
        for t in np.linspace(.0, 1, num=self._steps):
            cur = self.lerp(t)
            if t != .0:
                Drawer.drawLine(prev, cur, *self.color)
                totalLength += Point.dist(cur, prev)
            prev = cur
        self.length = totalLength
        glEnd()

    def lerp(self, t: float) -> Point:
        controlPointA = self.vertices[0] * (1-t) + self.vertices[1] * t
        controlPointB = self.vertices[1] * (1-t) + self.vertices[2] * t
        return controlPointA * (1-t) + controlPointB * t

    def derivative(self, t: float) -> Point:
        p0, p1, p2 = self.vertices
        return (p1 - p0) * 2 * (1-t) + (p2 - p1) * 2 * t
    
    def tangent(self, t: float) -> Point:
        return self.derivative(t).normalize()