from typing import List, Tuple

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Point import *
from src.BoundingBox import BoundingBox

class Polygon:
    def __init__(self, filepath: str = None, color: List[int] = [1, 1, 1], vertices: List[Point] = []):
        self.vertices: List[Point] = []
        if filepath is not None:
            points = Polygon.readFromFile(filepath)
            self.vertices.extend(points)
        if vertices is not None:
            self.vertices.extend(vertices)

        self.color = color
        bboxColor = [1 - c for c in color]
        self.bbox = BoundingBox(*self.getLimits(), bboxColor)

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

    def draw(self):
        glColor(*self.color)
        glBegin(GL_LINE_LOOP)
        for V in self.vertices:
            glVertex3f(V.x, V.y, V.z)
        glEnd()
