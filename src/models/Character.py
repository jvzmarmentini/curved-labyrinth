from dataclasses import dataclass

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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
    velocity: float = 1.

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

    def animate(self, delta):
        delta /= self.velocity

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

    def updateRotation(self) -> float:
        sense = self.position - self.prevPos
        norm = sense.normalize()
        angle = np.rad2deg(np.arccos(norm.y))
        if norm.x > 0:
            angle = 360 - angle
        self.rotation = angle

    def updateModel(self):
        self.updateRotation()

        animate = getattr(self.model, "animate", None)
        if callable(animate):
            animate()

    def bbox(self, drawFlag: bool = False) -> BoundingBox:
        bbox = self.model.bbox.transformations(
            self.rotation, self.scale, self.position
        )
        if drawFlag:
            self.drawBBox(bbox)
        return bbox

    def collided(self, other: BoundingBox, drawFlag) -> bool:
        # TODO: not working properly
        bbox = self.bbox(drawFlag)
        charBBox = other.bbox(drawFlag)
        return bbox.minEdge.x <= charBBox.minEdge.x and \
            bbox.maxEdge.x >= charBBox.maxEdge.x and \
            bbox.minEdge.y <= charBBox.minEdge.y and \
            bbox.maxEdge.y >= charBBox.maxEdge.y

    def drawBBox(self, bbox: BoundingBox):
        glPushMatrix()
        bbox.draw()
        glPopMatrix()

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glScalef(*self.scale)
        glRotatef(self.rotation, 0, 0, 1)
        self.model.draw()
        glPopMatrix()
