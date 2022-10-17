import math
from typing import Tuple

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from models.Point import Point
from models.Polygon import Polygon


class Train(Polygon):
    def __init__(self, *color):
        super().__init__(filepath="assets/cart.txt")
        self.color = color

    def drawEntity(self):
        glLineWidth(3)
        glColor3f(*self.color)
        self.draw()