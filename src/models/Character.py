from dataclasses import dataclass
from typing import Tuple
from typing_extensions import Self

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import src.helpers.settings as settings
from src.models.Curve import Curve
from src.models.Point import Point
from src.models.Polygon import Polygon


@dataclass
class Character:
    model: Polygon = None
    sense: Point = Point()
    angle: float = .0
    scale: Point = Point(1, 1, 1)

    t: float = .5
    direction: int = 0
    velocity: float = 2.
    handbreak: bool = False

    trail: Curve = None
    nextTrail: Tuple[Curve, bool] = None

    def __post_init__(self):
        self.model.scale(self.scale)

    def invertDirection(self):
        self.direction = not self.direction
        if self.nextTrail is not None:
            self.nextTrail[0].color = .5, .5, .5
            self.nextTrail = None

    def setNext(self, rot_dir):
        if self.nextTrail is not None:
            self.nextTrail[0].color = .5, .5, .5

        if self.t <= .5 and self.direction:
            self.trail.startNeighbours.rotate(rot_dir)
            self.nextTrail = self.trail.startNeighbours[0]
        if self.t >= .5 and not self.direction:
            self.trail.endNeighbours.rotate(rot_dir)
            self.nextTrail = self.trail.endNeighbours[0]

    def goToNext(self):
        self.trail.color = .5, .5, .5
        self.trail, invert = self.nextTrail
        self.direction = self.direction ^ (not invert)
        self.nextTrail = None
        self.t = self.direction

    def animate(self, time):
        if self.handbreak:
            return

        delta = self.velocity * time / self.trail.length

        if self.direction:
            self.t -= delta
            if self.t <= .5 and self.nextTrail is None:
                self.nextTrail = self.trail.randStartNeighbours()
            if self.t < 0:
                self.goToNext()
        else:
            self.t += delta
            if self.t >= .5 and self.nextTrail is None:
                self.nextTrail = self.trail.randEndNeighbours()
            if self.t > 1:
                self.goToNext()

        self.sense = self.trail.lerp(self.t)

        self.updateModel()
        self.updateRotation()

    def updateModel(self):
        animate = getattr(self.model, "animate", None)
        if callable(animate):
            animate()

    def updateRotation(self) -> float:
        sense = self.trail.derivative(self.t)
        norm = sense.normalize()
        angle = np.rad2deg(np.arccos(norm.y)) + 180 * self.direction
        self.angle = angle if norm.x <= 0 else 360 - angle

    def collided(self, other: Self) -> bool:
        bbox = self.model.bbox
        charBBox = other.model.bbox
        collisionOnX = bbox.minEdge.x >= charBBox.maxEdge.x and \
            bbox.maxEdge.x <= charBBox.minEdge.x
        collisionOnY = bbox.minEdge.y >= charBBox.maxEdge.y and \
            bbox.maxEdge.y <= charBBox.minEdge.y
        return collisionOnX and collisionOnY

    def display(self):
        self.model.rotate(self.angle)
        self.model.translate(self.sense)
        self.model.updateBBox()
        self.model.draw()
        if settings._debugger:
            self.model.bbox.draw()
        self.model.translate(Point() - self.sense)
        self.model.rotate(-self.angle)
