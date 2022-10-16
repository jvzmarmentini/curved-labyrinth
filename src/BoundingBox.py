from dataclasses import dataclass
from typing import List

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Point import Point


@dataclass
class BoundingBox():
    maxEdge: Point
    minEdge: Point
    color: List[float]
    interMax: Point = Point()
    interMin: Point = Point()

    def transformations(self, angle: float, scale: Point, sense: Point):
        newMin = self.minEdge
        newMin = newMin.rotate(angle)
        newMin = newMin.scale(scale)
        newMin = newMin.translate(sense)
        
        newMax = self.maxEdge
        newMax = newMax.rotate(angle)
        newMax = newMax.scale(scale)
        newMax = newMax.translate(sense)
        
        interMax = Point(self.minEdge.x, self.maxEdge.y)
        interMax = interMax.rotate(angle)
        interMax = interMax.scale(scale)
        interMax = interMax.translate(sense)
        
        interMin = Point(self.maxEdge.x, self.minEdge.y)
        interMin = interMin.rotate(angle)
        interMin = interMin.scale(scale)
        interMin = interMin.translate(sense)
        
        return BoundingBox(
            newMax, newMin, self.color, interMax, interMin
        )

    def draw(self):
        glColor(*self.color)
        glBegin(GL_LINE_LOOP)
        glVertex3f(*self.minEdge)
        glVertex3f(*self.interMax)
        glVertex3f(*self.maxEdge)
        glVertex3f(*self.interMin)
        glEnd()
        