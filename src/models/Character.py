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
    vector: Point = Point()
    angle: float = .0
    scale: Point = Point(1, 1, 1)

    t: float = .5
    sense: int = 0
    velocity: float = 2.
    handbreak: bool = False

    trail: Curve = None
    nextTrail: Tuple[Curve, bool] = None

    def __post_init__(self):
        self.model.scale(self.scale)

    def invertDirection(self):
        self.sense = not self.sense
        if self.nextTrail is not None:
            self.nextTrail[0].color = .5, .5, .5
            self.nextTrail[0].width = 2
            self.nextTrail = None

    def setNext(self, rot_dir):
        if self.nextTrail is not None:
            self.nextTrail[0].color = .5, .5, .5
            self.nextTrail[0].width = 2

        if self.t <= .5 and self.sense:
            self.trail.startNeighbours.rotate(rot_dir)
            self.nextTrail = self.trail.startNeighbours[0]
        if self.t >= .5 and not self.sense:
            self.trail.endNeighbours.rotate(rot_dir)
            self.nextTrail = self.trail.endNeighbours[0]

    def goToNext(self):
        self.trail.color = .5, .5, .5
        self.trail.width = 2
        self.trail, invert = self.nextTrail
        self.sense = self.sense ^ (not invert)
        self.nextTrail = None
        self.t = self.sense

    def animate(self, time):
        if self.handbreak:
            return

        delta = self.velocity * time / self.trail.length

        if self.sense:
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

        self.vector = self.trail.lerp(self.t)

        self.updateModel()
        self.updateRotation()

    def updateModel(self):
        animate = getattr(self.model, "animate", None)
        if callable(animate):
            animate()

    def updateRotation(self) -> float:
        deriv = self.trail.derivative(self.t)
        norm = deriv.normalize()
        angle = np.rad2deg(np.arccos(norm.y)) + 180 * self.sense
        self.angle = angle if norm.x <= 0 else - angle

    def collided(self, other: Self) -> bool:
        bbox = self.model.bbox
        charBBox = other.model.bbox
        collisionOnX = bbox.minEdge.x >= charBBox.maxEdge.x and \
            bbox.maxEdge.x <= charBBox.minEdge.x
        collisionOnY = bbox.minEdge.y >= charBBox.maxEdge.y and \
            bbox.maxEdge.y <= charBBox.minEdge.y
        return collisionOnX and collisionOnY

    def display(self):
        # glPushMatrix();
        # glTranslated(*self.vector);
        # glRotated(self.angle, 0, 0, 1);
        self.model.rotate(self.angle)
        self.model.translate(self.vector)
        self.model.updateBBox()
        self.model.draw()
        if settings._debugger:
            self.model.bbox.draw()
        self.model.translate(Point() - self.vector)
        self.model.rotate(-self.angle)
        # glPopMatrix();
