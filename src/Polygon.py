import copy
from typing import Tuple

from multipledispatch import dispatch
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from src.BoundingBox import BoundingBox

from src.Point import *


class Polygon:
    def __init__(self, *v: Point):
        self.vertices = []
        if v is not None:
            self.vertices.extend(v)

    def __len__(self):
        return len(self.vertices)

    def __str__(self) -> str:
        return '\n'.join([str(x) for x in self.vertices])

    @dispatch(float, float)
    def insertVertice(self, x: float, y: float) -> None:
        self.vertices.append(Point(x, y))

    @dispatch(Point)
    def insertVertice(self, p: Point) -> None:
        self.vertices.append(p)

    def getVertice(self, i) -> Point:
        return copy.deepcopy(self.vertices[i])

    def getLimits(self) -> Tuple[Point, Point]:
        assert len(self.vertices) > 0

        Min = copy.deepcopy(self.vertices[0])
        Max = copy.deepcopy(self.vertices[0])

        Min.x = min([v.x for v in self.vertices])
        Min.y = min([v.y for v in self.vertices])
        Min.z = min([v.z for v in self.vertices])

        Max.x = max([v.x for v in self.vertices])
        Max.y = max([v.y for v in self.vertices])
        Max.z = max([v.z for v in self.vertices])

        return Min, Max

    def modifyVertice(self, i, P):
        self.vertices[i] = P

    def getEdge(self, n: int) -> Point:
        v1 = self.vertices[n]
        v2 = self.vertices[(n+1) % len(self)]
        return v2 - v1
