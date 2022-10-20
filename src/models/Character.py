from dataclasses import dataclass

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import src.helpers.settings as settings
from src.models.BoundingBox import BoundingBox
from src.models.Curve import Curve
from src.models.Point import Point
from src.models.Polygon import Polygon


@dataclass
class Character:
    model: Polygon = None
    isPlayer: bool = False
    position: Point = Point()
    prevPos: Point = Point()
    rotation: float = .0
    scale: Point = Point(1, 1, 1)

    t: float = .0
    direction: int = 0
    velocity: float = 2.

    trail: Curve = None
    nextTrail = None

    def __str__(self) -> str:
        return f"{id(self)}"

    def invertDirection(self):
        self.direction = not self.direction
        if self.nextTrail is not None:
            self.nextTrail.curve.color = .5, .5, .5
            self.nextTrail = None

    def setNext(self, rot_dir):
        if self.nextTrail is not None:
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

    def animate(self, time):
        delta = self.velocity * time / self.trail.length

        if self.direction:
            self.t -= delta
            if self.t <= .5 and self.nextTrail is None:
                self.nextTrail = self.trail.randLowNeighbours()
            if self.t < 0:
                self.goToNext()
        else:
            self.t += delta
            if self.t >= .5 and self.nextTrail is None:
                self.nextTrail = self.trail.randUpNeighbours()
            if self.t > 1:
                self.goToNext()

        self.prevPos = self.position
        self.position = self.trail.lerp(self.t)

        self.updateModel()
        self.updateRotation()
        # updateVertices()
        # updateAABB()

    def updateModel(self):
        animate = getattr(self.model, "animate", None)
        if callable(animate):
            animate()

    def updateRotation(self) -> float:
        sense = self.position - self.prevPos
        norm = sense.normalize()
        angle = np.rad2deg(np.arccos(norm.y))
        self.rotation = angle if norm.x <= 0 else 360 - angle

    def collided(self, other: BoundingBox) -> bool:
        # TODO: not working properly
        bbox = self.model.bbox
        if settings._debugger:
            bbox.draw()
        charBBox = other.model.bbox
        if settings._debugger:
            charBBox.draw()
        collisionOnX = charBBox.minEdge.x <= bbox.maxEdge.x and charBBox.maxEdge.x >= bbox.minEdge.x
        collisionOnY = charBBox.minEdge.y <= bbox.maxEdge.y and charBBox.maxEdge.y >= bbox.minEdge.y
        return collisionOnX and collisionOnY

    def draw(self):
        poly = self.model.updateVertices(
            self.rotation, self.scale, self.position)
        poly.draw()
