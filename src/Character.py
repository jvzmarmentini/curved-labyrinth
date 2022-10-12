
from typing import List

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from typing_extensions import Self

from src.Curve import Curve
from src.Drawer import Drawer
from src.Point import Point


class Character:
    def __init__(self, model=None, scale: float = Point(1, 1, 1), velocity: float = 2.0) -> None:
        self.model = model
        self.position = Point()
        self.scale = scale
        self.rotation = .0

        self.t = .0
        self.direction = 0
        self.velocity = velocity

        self.maxEdge = [v * s for v,
                        s in zip(self.model.getLimitsMax(), scale)]
        self.minEdge = [v * s for v,
                        s in zip(self.model.getLimitsMin(), scale)]
        self.boundingBox = None

        self.trail = None
        self.nextTrail = None

    def __str__(self) -> str:
        return f"{id(self)}"

    def setTrail(self, trail: Curve, direction: bool = False):
        self.trail = trail
        self.direction = direction

    def invertDirection(self):
        self.direction = not self.direction
        if self.nextTrail is not None:
            self.nextTrail.curve.color = .5, .5, .5
            self.nextTrail = None

    def animate(self, et):
        et /= self.velocity * 1000

        if self.direction:
            self.t -= et
            if self.t <= .5 and self.nextTrail is None:
                self.nextTrail = self.trail.randLowNeighbours()
            if self.t <= .0:
                self.trail.color = .5, .5, .5
                self.trail, invert = self.nextTrail
                self.direction = self.direction ^ invert
                self.nextTrail = None
                self.t = self.direction
        else:
            self.t += et
            if self.t >= .5 and self.nextTrail is None:
                self.nextTrail = self.trail.randUpNeighbours()
            if self.t >= 1.:
                self.trail.color = .5, .5, .5
                self.trail, invert = self.nextTrail
                self.direction = self.direction ^ invert
                self.nextTrail = None
                self.t = self.direction
        self.position = self.trail.lerp(self.t)

        self.updateModel()

    def updateModel(self):
        animate = getattr(self.model, "animate", None)
        if callable(animate):
            animate()

        self.boundingBox = (self.position + self.minEdge,
                            self.position + self.maxEdge)

    def collision(self, enemies: List[Self]):
        # TODO: test collision
        pass

    def draw(self):
        Drawer.drawBBox(self.boundingBox, 1, 1, 0)
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.scale.x, self.scale.y, self.scale.z)
        self.model.drawEntity()
        glPopMatrix()
