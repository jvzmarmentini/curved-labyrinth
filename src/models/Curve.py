from dataclasses import dataclass, field
import random
from collections import deque
from typing import Deque, List, Tuple

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from typing_extensions import Self

import src.helpers.settings as settings
from src.helpers.Drawer import Drawer
from src.models.Point import Point
from src.models.Polygon import Polygon


@dataclass
class Curve(Polygon):
    _steps = 15
    
    startNeighbours: Deque[Tuple[Self, int]] = field(default_factory=deque)
    endNeighbours: Deque[Tuple[Self, int]] = field(default_factory=deque)
    
    color: List[int] = field(default_factory=lambda: [.5, .5, .5])
    width: int = 2
    
    length: float = 0
    
    @property
    def steps(self):
        return self.__class__._steps
    @steps.setter
    def steps(self, value):
        self.__class__._steps = value

    def randStartNeighbours(self):
        return random.choice(list(self.startNeighbours))

    def randEndNeighbours(self):
        return random.choice(list(self.endNeighbours))

    def generate(self) -> None:
        if settings._debugger:
            Drawer.drawCoords(self.lerp(0))
            Drawer.drawCoords(self.lerp(1))
        
        totalLength = 0
        for t in np.linspace(.0, 1, num=self._steps):
            cur = self.lerp(t)
            if t != .0:
                Drawer.drawLine(prev, cur, self.width, *self.color)
                totalLength += Point.dist(cur, prev)
            prev = cur
        self.length = totalLength
        

    def lerp(self, t: float) -> Point:
        controlPointA = self.vertices[0] * (1-t) + self.vertices[1] * t
        controlPointB = self.vertices[1] * (1-t) + self.vertices[2] * t
        return controlPointA * (1-t) + controlPointB * t

    def derivative(self, t: float) -> Point:
        p0, p1, p2 = self.vertices
        return (p1 - p0) * 2 * (1-t) + (p2 - p1) * 2 * t
    
    def tangent(self, t: float) -> Point:
        return self.derivative(t).normalize()