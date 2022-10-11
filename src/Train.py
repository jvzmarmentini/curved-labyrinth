from operator import mul
from typing import Tuple
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Point import Point
from src.Polygon import Polygon


class Train(Polygon):
    def __init__(self, color):
        super().__init__(filepath="assets/cart.txt")
        self.color = color

    def getBBox(self, scale: Point) -> Tuple[Point, Point]:
        return [(Point(*[p * s for p, s in zip(point, scale)])) for point in self.getLimits()]

    def drawEntity(self):
        glLineWidth(3)
        glPushMatrix()
        glColor3f(*self.color)
        self.draw()
        glPopMatrix()
