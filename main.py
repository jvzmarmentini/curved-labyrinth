# -*- coding: utf-8 -*-
import argparse
import os

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Character import Character
from src.Curve import Curve
from src.Drawer import *
from src.Polygon import *
from src.Train import Train

flagDrawAxis = True
scene = None
curves = []
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

    characters["player"] = Character(model=Train(color=[1, 0, 1]), scale=Point(.5,.5,1))
    curves[0].getOnRails(characters["player"])

    # for idx in range(1):
    #     name = f"enemy{idx}"
    #     characters[name] = Character(model=Windmill(color=[0,1,1]))
    #     startCurveIdx = random.randint(0, len(curves) - 1)
    #     curves[startCurveIdx].getOnRails(characters[name])


def init() -> None:
    global scene

    minPoint = Point(-6, -6, 0)
    maxPoint = Point(6, 6, 0)
    scene = Polygon(None, minPoint, maxPoint)
    initCurves()
    initCharacters()


def reshape(w, h):
    minPoint, maxPoint = scene.getLimits()

    glViewport(minPoint.x, minPoint.y, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(minPoint.x, maxPoint.x,
            minPoint.y, maxPoint.y, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


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
    et = glutGet(GLUT_ELAPSED_TIME) % 1000 / 1000

    for char in characters.values():
        char.updateModel()

    for curve in curves:
        curve.animate(et)

    glutPostRedisplay()


def keyboard(*args) -> None:
    if args[0] == b'q' or args[0] == b'\x1b':
        os._exit(0)
    if args[0].isspace():
        print("space")

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
