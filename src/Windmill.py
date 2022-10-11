from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Point import Point
from src.Polygon import Polygon


class Windmill(Polygon):
    def __init__(self, color, *v: Point):
        super().__init__(*v)
        self.tower = Polygon(filepath="assets/tower.txt")
        self.halfBlade = Polygon(filepath="assets/halfBlade.txt")
        self.bladeAngle = 1
        self.color = color

    def animate(self) -> None:
        self.bladeAngle += 1

    def drawSingelBlade(self):
        glPushMatrix()
        glTranslated(-4, 0, 0)
        self.halfBlade.draw()
        glScaled(1, -1, 1)
        self.halfBlade.draw()
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
        glColor3f(*self.color)
        self.drawTower()
        glPushMatrix()
        towerMaxY = self.tower.getLimitsMax().y
        glTranslated(0, towerMaxY, 0)
        glScaled(0.2, 0.2, 1)
        self.drawRotatingBlades()
        glPopMatrix()
        glPopMatrix()
