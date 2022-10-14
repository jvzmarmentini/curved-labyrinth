from collections import namedtuple
from dataclasses import dataclass

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Curve import Curve
from src.Point import Point
from src.Polygon import Polygon


@dataclass
class Character:
    model: Polygon = None
    isPlayer: bool = False
    position: Point = Point()
    scale: Point = Point(1, 1, 1)
    rotation: float = .0

    t: float = .0
    direction: int = False
    velocity: float = 2.
    
    maxEdge: Point = None
    minEdge: Point = None
    boundingBox = None

    trail: Curve = None
    nextTrail = None

    def __post_init__(self):
        self.maxEdge = self.model.getLimitsMax(self.scale)
        self.minEdge = self.model.getLimitsMin(self.scale)

    def __str__(self) -> str:
        return f"{id(self)}"

    def invertDirection(self):
        self.direction = not self.direction
        if self.nextTrail is not None:
            self.nextTrail.curve.color = .5, .5, .5
            self.nextTrail = None

    def setNext(self, rot_dir):
        self.nextTrail.curve.color = .5, .5, .5

        if self.t <= .5 and self.direction:
            self.trail.lowNeighbours.rotate(rot_dir)
            self.nextTrail = self.trail.lowNeighbours[0]
        if self.t >= .5 and not self.direction:
            self.nextTrail.curve.color = .5, .5, .5
            self.trail.upNeighbours.rotate(rot_dir)
            self.nextTrail = self.trail.upNeighbours[0]

    def goToNext(self):
        self.trail.color = .5, .5, .5
        self.trail, invert = self.nextTrail
        self.direction = self.direction ^ invert
        self.nextTrail = None
        self.t = self.direction

    def animate(self, delta):
        delta /= self.velocity * 1000

        if self.direction:
            self.t -= delta
            if self.t <= .5 and self.nextTrail is None:
                self.nextTrail = self.trail.randLowNeighbours()
            if self.t <= .0:
                self.goToNext()
        else:
            self.t += delta
            if self.t >= .5 and self.nextTrail is None:
                self.nextTrail = self.trail.randUpNeighbours()
            if self.t >= 1.:
                self.goToNext()

        self.position = self.trail.lerp(self.t)

        self.updateModel()

    def updateRotation(self) -> float:
        normSense = self.trail.normalize(self.t)
        normY = Point(0, -1, 0)
        dot = normSense.dot(normY)
        abMag = normSense.magnitude() * normY.magnitude()
        angle = np.arccos(dot/abMag)
        self.rotation = np.rad2deg(angle) + self.direction * 180

    def updateModel(self):
        animate = getattr(self.model, "animate", None)
        if callable(animate):
            animate()

        Limits = namedtuple("Limits", "min max")
        self.boundingBox = Limits(self.position + self.minEdge,
                                  self.position + self.maxEdge)

        self.updateRotation()

    def draw(self):
        # Drawer.drawBBox(self.boundingBox, 1, 1, 0)
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.scale.x, self.scale.y, self.scale.z)
        self.model.drawEntity()
        glPopMatrix()
