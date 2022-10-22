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
    
    def update(self, maxEdge: Point, minEdge: Point):
        self.maxEdge = maxEdge
        self.minEdge = minEdge

    def draw(self):
        glColor(*self.color)
        glBegin(GL_LINE_LOOP)
        glVertex3f(*self.minEdge)
        glVertex3f(self.minEdge.x, self.maxEdge.y, 0)
        glVertex3f(*self.maxEdge)
        glVertex3f(self.maxEdge.x, self.minEdge.y, 0)
        glEnd()
