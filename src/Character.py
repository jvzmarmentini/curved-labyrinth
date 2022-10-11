
from typing import List
from typing_extensions import Self
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Drawer import Drawer
from src.Point import Point


class Character:
    def __init__(self, model=None, position: float = Point(), scale: float = Point(1, 1, 1), rotation=.0, t: float = .0, isPlayer: bool = False) -> None:
        self.model = model
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.t = t
        self.direction = 0
        self.isPlayer = isPlayer

        self.maxEdge = [v * s for v,
                        s in zip(self.model.getLimitsMax(), scale)]
        self.minEdge = [v * s for v,
                        s in zip(self.model.getLimitsMin(), scale)]
        self.boundingBox = None

    def __str__(self) -> str:
        return f"{id(self)}"

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
        # Drawer.drawBBox(self.boundingBox, 1, 1, 0)
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.scale.x, self.scale.y, self.scale.z)
        self.model.drawEntity()
        glPopMatrix()
