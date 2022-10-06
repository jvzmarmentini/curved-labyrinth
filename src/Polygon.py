import copy
from typing import Tuple

from multipledispatch import dispatch
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Point import *


class Polygon:
    def __init__(self, filepath: str = None, *v: Point):
        self.vertices = []
        if filepath is not None:
            points = Polygon.readFromFile(filepath)
            self.vertices.extend(points)
        if v is not None:
            self.vertices.extend(v)

    def __len__(self):
        return len(self.vertices)

    def __str__(self) -> str:
        return '\n'.join([str(x) for x in self.vertices])

    @staticmethod
    def readFromFile(filepath: str):
        points = []
        with open(filepath) as f:
            for line in f:
                coord = list(map(float, line.split()))
                points.append(Point(*coord))
        return points

    @dispatch(float, float)
    def insertVertice(self, x: float, y: float) -> None:
        self.vertices.append(Point(x, y))

    @dispatch(Point)
    def insertVertice(self, p: Point) -> None:
        self.vertices.append(p)

    def getVertice(self, i) -> Point:
        return copy.deepcopy(self.vertices[i])

    def getLimitsMin(self) -> Point:
        assert len(self.vertices) > 0
        return Point(min([v.x for v in self.vertices]),
                     min([v.y for v in self.vertices]),
                     min([v.z for v in self.vertices]))

    def getLimitsMax(self) -> Point:
        assert len(self.vertices) > 0
        return Point(max([v.x for v in self.vertices]),
                     max([v.y for v in self.vertices]),
                     max([v.z for v in self.vertices]))

    def getLimits(self) -> Tuple[Point, Point]:
        return self.getLimitsMin(), self.getLimitsMax()

    def modifyVertice(self, i, P):
        self.vertices[i] = P

    def getEdge(self, n: int) -> Point:
        v1 = self.vertices[n]
        v2 = self.vertices[(n+1) % len(self)]
        return v2 - v1

    def draw(self):
        glBegin(GL_LINE_LOOP)
        for V in self.vertices:
            glVertex3f(V.x, V.y, V.z)
        glEnd()
