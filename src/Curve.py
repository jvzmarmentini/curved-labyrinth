from typing import Iterator, Tuple
import numpy as np

from src.Point import Point
from src.Polygon import Polygon


class Curve(Polygon):
    def __init__(self, *v):
        super().__init__(*v)
        self.curvePoints = []
        self.generateCurvePoints()
        
    def __len__(self):
        return len(self.curvePoints)

    def getEdges(self) -> Iterator[Tuple[Point,Point,float]]:
        for i in range(len(self) - 1):
            v1 = self.curvePoints[i]
            v2 = self.curvePoints[i+1]
            yield v2, v1, i/99

    def generateCurvePoints(self):
        for t in np.linspace(0, 1, num=101):
            self.curvePoints.append(self.lerp(t))

    def lerp(self, t: float) -> Point:
        controlPointA = self.vertices[0] * (1-t) + self.vertices[1] * t
        controlPointB = self.vertices[1] * (1-t) + self.vertices[2] * t
        return controlPointA * (1-t) + controlPointB * t

    def draw(self):
        pass
