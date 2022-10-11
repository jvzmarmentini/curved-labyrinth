from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Polygon import Polygon
from src.Point import Point
from src.Drawer import Drawer


class Character:
    def __init__(self, model=None, position=Point(), scale=Point(1, 1, 1), rotation=.0, t=.0) -> None:
        self.model = model
        self.boundingBox = (self.model.getLimits(scale))
        self.position = position
        self.relativePos = position
        self.scale = scale
        self.rotation = rotation
        self.t = t
        self.direction = 0
        
    def __str__(self) -> str:
        return f"{id(self)}"
        
    def updateModel(self):
        animate = getattr(self.model, "animate", None)
        if callable(animate):
            animate()
            
        self.relativePos -= self.position

    def draw(self):
        Drawer.drawBBox(self.boundingBox, 1, 1, 0)
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.scale.x, self.scale.y, self.scale.z)
        self.model.drawEntity()
        glPopMatrix()
