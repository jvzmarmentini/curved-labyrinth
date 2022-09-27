from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from src.Polygon import Polygon

from src.Point import *


class Drawer():
    @staticmethod
    def drawAxis(scene: Polygon) -> None:
        minPoint, maxPoint = scene.getLimits()
        mid = (maxPoint - minPoint) * .5
        glLineWidth(1)
        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        glVertex2f(minPoint.x, mid.y)
        glVertex2f(maxPoint.x, mid.y)
        glVertex2f(mid.x, minPoint.y)
        glVertex2f(mid.x, maxPoint.y)
        glEnd()