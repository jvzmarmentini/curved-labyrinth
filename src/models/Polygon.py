from dataclasses import dataclass, field
from typing import List, Tuple

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.models.BoundingBox import BoundingBox
from src.models.Point import Point


@dataclass
class Polygon:
    vertices: List[Point] = field(default_factory=list)
    filepath: str = None
    color: List[int] = field(default_factory=lambda: [1, 1, 1])

    def __post_init__(self):
        if self.filepath is not None:
            self.extendFromFile()
        self.bbox = BoundingBox(*self.getLimits(), [1 - c for c in self.color])

    def __iter__(self):
        return iter(self.vertices)

    def __getitem__(self, item):
        return self.vertices[item]

    def __len__(self):
        return len(self.vertices)

    def __str__(self) -> str:
        return '\n'.join([str(x) for x in self.vertices])

    def extendFromFile(self) -> None:
        with open(self.filepath) as f:
            self.vertices.extend(
                [Point(*map(float, line.split())) for line in f]
            )

    def getLimitsMin(self) -> Point:
        assert len(self) > 0
        return Point(min([v.x for v in self]),
                     min([v.y for v in self]),
                     min([v.z for v in self]))

    def getLimitsMax(self) -> Point:
        assert len(self) > 0
        return Point(max([v.x for v in self]),
                     max([v.y for v in self]),
                     max([v.z for v in self]))

    def getLimits(self) -> Tuple[Point, Point]:
        return self.getLimitsMin(), self.getLimitsMax()

    def scale(self, scale: Point = Point(1, 1, 1)):
        self.vertices = [v.scale(scale) for v in self]

    def translate(self, sense: Point = Point()):
        self.vertices = [v.translate(sense) for v in self]

    def rotate(self, angle: float = 0):
        self.vertices = [v.rotate(angle) for v in self]

    def updateBBox(self):
        self.bbox.update(*self.getLimits())

    def draw(self):
        glColor(*self.color)
        glBegin(GL_LINE_LOOP)
        [glVertex3f(v.x, v.y, v.z) for v in self.vertices]
        glEnd()
