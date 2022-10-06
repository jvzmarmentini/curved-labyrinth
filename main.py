# -*- coding: utf-8 -*-
import argparse
import os
from select import POLLHUP

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Character import Character
from src.Curve import Curve
from src.Drawer import *
from src.Polygon import *
from src.Windmill import Windmill

flagDrawAxis = True
scene = None
curves = None
characters = {}


def initCurves() -> None:
    global curves

    points = []
    with open("./assets/basePoints.txt") as f:
        for line in f:
            coord = list(map(float, line.split()))
            x = coord[0]
            y = coord[1]
            points.append(Point(x, y))

    curves = []
    refs = []
    with open("./assets/curves.txt") as f:
        for line in f:
            vertices = [points[i] for i in map(int, line.split())]
            curve = Curve(None, *vertices)
            curves.append(curve)
            refs.append(line.split())
            del refs[-1][1]

    for ref, curve in zip(refs, curves):
        for ref2, curve2 in zip(refs, curves):
            if curve == curve2:
                continue
            if ref[0] == ref2[0]:
                curve.lowerNeighbours.add((curve2, 1))
            if ref[0] == ref2[1]:
                curve.lowerNeighbours.add((curve2, 0))
            if ref[1] == ref2[0]:
                curve.upperNeighbours.add((curve2, 0))
            if ref[1] == ref2[1]:
                curve.upperNeighbours.add((curve2, 1))


def initCharacters() -> None:
    global characters

    # characters["char1"] = Character(model=Windmill())
    characters["char2"] = Character(model=Windmill())
    curves[0].getOnRails(characters["char2"])


def reshape(w, h):
    minPoint, maxPoint = scene.getLimits()

    glViewport(minPoint.x, minPoint.y, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(minPoint.x, maxPoint.x,
            minPoint.y, maxPoint.y, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def init() -> None:
    global scene

    minPoint = Point(-5, -5, 0)
    maxPoint = Point(5, 5, 0)
    scene = Polygon(None, minPoint, maxPoint)
    initCurves()
    initCharacters()


def display() -> None:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if (flagDrawAxis):
        Drawer.drawAxis(scene)

    for curve in curves:
        curve.generate()

    for char in characters.values():
        char.draw()

    glutSwapBuffers()
    
def animate():
    et = glutGet(GLUT_ELAPSED_TIME) % 10000 / 10000
    
    for char in characters.values():
        char.updateModel()
    
    for curve in curves:
        curve.animate(et)
    glutPostRedisplay()


def keyboard(*args) -> None:
    if args[0] == b'q' or args[0] == b'\x1b':
        os._exit(0)

    glutPostRedisplay()


def main() -> None:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(900, 900)

    glutCreateWindow("Pontos no Triangulo")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    init()

    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    try:
        glutMainLoop()
    except SystemExit:
        pass


if __name__ == '__main__':
    main()
