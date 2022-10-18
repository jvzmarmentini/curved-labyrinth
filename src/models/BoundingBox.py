from dataclasses import dataclass
from typing import List

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.models.Point import Point


@dataclass
class BoundingBox():
    maxEdge: Point
    minEdge: Point
    color: List[float]
    interMax: Point = Point()
    interMin: Point = Point()

    def transformations(self, angle: float = .0, scale: Point = Point(1,1,1), sense: Point = Point()):
        newMin = self.minEdge.apply(angle,scale,sense)

        newMax = self.maxEdge.apply(angle,scale,sense)

        interMax = Point(self.minEdge.x, self.maxEdge.y).apply(angle,scale,sense)

        interMin = Point(self.maxEdge.x, self.minEdge.y).apply(angle,scale,sense)

        return BoundingBox(
            newMax, newMin, self.color, interMax, interMin
        )

    def draw(self):
        glColor(*self.color)
        glBegin(GL_LINE_LOOP)
        glVertex3f(*self.minEdge)
        glVertex3f(self.minEdge.x, self.maxEdge.y, 0)
        # glVertex3f(*self.interMax)
        glVertex3f(*self.maxEdge)
        glVertex3f(self.maxEdge.x, self.minEdge.y, 0)
        # glVertex3f(*self.interMin)
        glEnd()
