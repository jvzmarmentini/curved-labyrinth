from typing import Iterator, Tuple

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Drawer import Drawer
from src.Point import Point
from src.Polygon import Polygon


class Curve(Polygon):
    def __init__(self, *v):
        super().__init__(*v)
        self.lowerNeighbours = set()
        self.upperNeighbours = set()

    def __len__(self):
        return len(self.curvePoints)

    def generate(self):
        Drawer.drawCoords(self.lerp(0))
        glLineWidth(4)
        glBegin(GL_LINES)
        for t in np.linspace(.0, 1, num=101):
            cur = self.lerp(t)
            if t != .0:
                color = prev.x, prev.y, max(t, .5)
                Drawer.drawLine(prev, cur, *color)
            prev = cur
        glEnd()

    def lerp(self, t: float) -> Point:
        controlPointA = self.vertices[0] * (1-t) + self.vertices[1] * t
        controlPointB = self.vertices[1] * (1-t) + self.vertices[2] * t
        return controlPointA * (1-t) + controlPointB * t

