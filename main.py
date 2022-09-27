# -*- coding: utf-8 -*-
import argparse
import os
from select import POLLHUP

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Drawer import *
from src.Polygon import *
from src.Curve import Curve

flagDrawAxis = False
scene = None
curves = None


def readCurvesFromFile() -> None:
    global curves
    
    points = []
    with open("./assets/basePoints.txt") as f:
        for line in f:
            coord = list(map(float, line.split()))
            x = coord[0]
            y = coord[1]
            points.append(Point(x, y))

    curves = []
    with open("./assets/curves.txt") as f:
        for line in f:
            vertices = [points[i] for i in map(int, line.split())]
            curve = Curve(*vertices)
            curves.append(curve)

def init() -> None:
    global scene

    minPoint = Point(-5, -5, 0)
    maxPoint = Point(5, 5, 0)
    scene = Polygon(minPoint, maxPoint)
    readCurvesFromFile()


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
        Drawer.drawCurve(curve)

    glutSwapBuffers()
    # glutPostRedisplay()


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
    init()

    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    try:
        glutMainLoop()
    except SystemExit:
        pass


if __name__ == '__main__':
    main()
