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
        
    def getBBox(self, scale: Point) -> Tuple[Point,Point]:
        # lMin, lMax = self.getLimits()
        # lMin.x *= scale.x
        # lMin.y *= scale.y
        # lMin.z *= scale.z
        pass
        # return [map(mul, x, scale) for x in self.cart.getLimits()]

    def drawEntity(self):
        glLineWidth(3)
        glPushMatrix()
        glColor3f(*self.color)
        self.draw()
        glPopMatrix()
