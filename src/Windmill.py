from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from typing_extensions import Self

from src.Point import Point
from src.Polygon import Polygon


class Windmill(Polygon):
    def __init__(self, *v: Point):
        super().__init__(*v)
        # self.min, self.max = self.getLimits()
        self.tower = Polygon(filepath="assets/tower.txt")
        self.halfBlades = Polygon(filepath="assets/halfBlade.txt")
        self.bladeAngle = 1

    def animate(self) -> None:
        self.bladeAngle += 1

    def collision(self, bbox: Self) -> bool:
        return self.min.x <= bbox.max.x and self.max.x >= bbox.min.x and (
            self.min.y <= bbox.max.y and self.max.y >= bbox.min.y)

    def drawSingelBlade(self):
        glPushMatrix()
        glTranslated(-4, 0, 0)
        self.halfBlades.draw()
        glScaled(1,-1, 1)
        self.halfBlades.draw()
        glPopMatrix()

    def drawBlades(self):
        glPushMatrix()
        for _ in range(4):
            glRotatef(90, 0, 0, 1)
            self.drawSingelBlade()
        glPopMatrix()

    def drawRotatingBlades(self):
        glPushMatrix()
        glRotatef(self.bladeAngle, 0, 0, 1)
        self.drawBlades()
        glPopMatrix()

    def drawTower(self):
        self.tower.draw()

    def drawEntity(self):
        glLineWidth(3)
        glPushMatrix()
        self.drawTower()
        glPushMatrix()
        glColor3f(1, 0, 0)
        towerMaxY = self.tower.getLimitsMax().y
        glTranslated(0, towerMaxY, 0)
        glScaled(0.2, 0.2, 1)
        self.drawRotatingBlades()
        glPopMatrix()
        glPopMatrix()
