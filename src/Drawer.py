from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Curve import Curve
from src.Point import *
from src.Polygon import Polygon


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

    @staticmethod
    def displayTitle(string: str, x: float, y: float):
        glColor3f(1, 1, 1)
        glRasterPos2f(x, y)
        for c in string:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))

    @staticmethod
    def drawCurve(curve: Curve):
        for prev, cur, t in curve.getEdges():
            glLineWidth(4)
            glColor3f(cur.x, cur.y, max(t, .5))
            glBegin(GL_LINES)
            glVertex2f(prev.x, prev.y)
            glVertex2f(cur.x, cur.y)
            glEnd()
            if t == 0:
                Drawer.displayTitle(f"({cur.x:.0f},{cur.y:.0f})", cur.x, cur.y)