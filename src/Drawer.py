from typing import Mapping, Tuple
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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
    def displayText(string: str, x: float, y: float, *color):
        if color is not None:
            glColor3f(*color)
        glRasterPos2f(x, y)
        for c in string:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))

    @staticmethod
    def drawLine(p1: Point, p2: Point, *color):
        if color is not None:
            glColor3f(*color)
        glVertex2f(p1.x, p1.y)
        glVertex2f(p2.x, p2.y)

    @staticmethod
    def drawCoords(p: Point, *color):
        if color is not None:
            color = 1, 1, 1
        Drawer.displayText(f"({p.x:.0f},{p.y:.0f})", p.x, p.y, *color)

    @staticmethod
    def drawPolygon(vertices: Polygon, *color):
        if color is not None:
            glColor3f(*color)
        glBegin(GL_LINE_LOOP)
        for vertice in vertices:
            glVertex3f(vertice.x, vertice.y, vertice.z)
        glEnd()

    @staticmethod
    def drawBBox(bbox: Mapping, *color):
        if color is not None:
            glColor3f(*color)
        glBegin(GL_LINE_LOOP)
        bbox = list(bbox)
        glVertex3f(bbox[0].x, bbox[0].y, bbox[0].z)
        glVertex3f(bbox[0].x, bbox[1].y, bbox[0].z)
        glVertex3f(bbox[1].x, bbox[1].y, bbox[0].z)
        glVertex3f(bbox[1].x, bbox[0].y, bbox[0].z)
        glEnd()