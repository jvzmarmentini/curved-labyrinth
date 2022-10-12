import random
from typing import List, Set

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Character import Character
from src.Drawer import Drawer
from src.Point import Point
from src.Polygon import Polygon


class Curve(Polygon):
    def __init__(self, *v):
        super().__init__(*v)
        self.lowerNeighbours: Set[Character] = set()
        self.upperNeighbours: Set[Character] = set()
        self.charsOnRails: List[Character] = []

    def __len__(self) -> int:
        return len(self.curvePoints)

    def __str__(self) -> str:
        return f"Curve={id(self)}, OnRails={list(map(str,self.charsOnRails))}"

    def getOnRails(self, char: Character):
        self.charsOnRails.append(char)

    def animate(self, et: float) -> None:
        for char in self.charsOnRails:
            if char.isPlayer:
                char.collision(self.charsOnRails)
            if char.direction:
                char.t -= et
                if char.t <= .5:
                    # TODO: choose next
                    pass
                if char.t <= 1:
                    # TODO: change to next
                    pass
            else:
                char.t += et
                if char.t >= .5:
                    # TODO: choose next
                    pass
                if char.t >= 1:
                    # TODO: change to next
                    pass
            # if et < char.t:
            #     if not char.direction:
            #         chosen, invert = random.choice(list(self.upperNeighbours))
            #     else:
            #         chosen, invert = random.choice(list(self.lowerNeighbours))
            #     char.direction = char.direction ^ invert
            #     self.charsOnRails.remove(char)
            #     chosen.getOnRails(char)
            # else:
            char.position = self.lerp(char.t)
        

    def generate(self) -> None:
        Drawer.drawCoords(self.lerp(0))
        Drawer.drawCoords(self.lerp(1))
        glLineWidth(4)
        glBegin(GL_LINES)
        for t in np.linspace(.0, 1, num=101):
            cur = self.lerp(t)
            if t != .0:
                color = prev.x, prev.y, max(t, .5)
                Drawer.drawLine(prev, cur, *color)
            prev = cur
        glEnd()

    def lerp(self, t: float) -> Point:
        controlPointA = self.vertices[0] * (1-t) + self.vertices[1] * t
        controlPointB = self.vertices[1] * (1-t) + self.vertices[2] * t
        return controlPointA * (1-t) + controlPointB * t
