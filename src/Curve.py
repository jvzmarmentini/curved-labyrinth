
import numpy as np
import random
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
        self.lowerNeighbours = set()
        self.upperNeighbours = set()
        self.charsOnRails = []

    def __len__(self):
        return len(self.curvePoints)

    def __str__(self) -> str:
        return f"Curve={id(self)}, OnRails={list(map(str,self.charsOnRails))}"

    def getOnRails(self, char: Character):
        self.charsOnRails.append(char)

    def animate(self, et):
        for char in self.charsOnRails:
            normalET = round(abs(char.direction - et), 5)
            prevT = char.t

            if not char.direction and normalET < prevT:
                chosen, invert = random.choice(list(self.upperNeighbours))
                char.direction = char.direction ^ invert
                char.t = round(abs(invert - normalET), 5)
                self.charsOnRails.remove(char)
                chosen.getOnRails(char)
                continue

            if char.direction and normalET > prevT:
                chosen, invert = random.choice(list(self.lowerNeighbours))
                char.direction = char.direction ^ invert
                char.t = round(abs(invert - normalET), 5)
                self.charsOnRails.remove(char)
                chosen.getOnRails(char)
                continue

            char.t = normalET
            char.position = self.lerp(normalET)

    def generate(self):
        Drawer.drawCoords(self.lerp(0))
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
