from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Point import Point


class Character:
    def __init__(self, model=None, position=Point(), scale=Point(1, 1, 1), rotation=.0, t=.0) -> None:
        self.model = model
        self.position = position
        self.scale = scale
        self.rotation = rotation
        self.t = t
        self.direction = 0
        
    def updateModel(self):
        self.model.animate()

    def draw(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.scale.x, self.scale.y, self.scale.z)
        self.model.drawEntity()
        glPopMatrix()
