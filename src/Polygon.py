from typing import Tuple

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

    def insertVertice(self, p: Point) -> None:
        self.vertices.append(p)

    def getLimitsMin(self, scale: Point = Point(1, 1, 1)) -> Point:
        assert len(self.vertices) > 0
        return Point(min([v.x for v in self.vertices]) * scale.x,
                     min([v.y for v in self.vertices]) * scale.y,
                     min([v.z for v in self.vertices]) * scale.z)

    def getLimitsMax(self, scale: Point = Point(1, 1, 1)) -> Point:
        assert len(self.vertices) > 0
        return Point(max([v.x for v in self.vertices]) * scale.x,
                     max([v.y for v in self.vertices]) * scale.y,
                     max([v.z for v in self.vertices]) * scale.z)

    def getLimits(self) -> Tuple[Point, Point]:
        return self.getLimitsMin(), self.getLimitsMax()

    def draw(self):
        glBegin(GL_LINE_LOOP)
        for V in self.vertices:
            glVertex3f(V.x, V.y, V.z)
        glEnd()
