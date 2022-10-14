# -*- coding: utf-8 -*-
import argparse
import os
from collections import namedtuple
from random import choice, getrandbits, uniform
from typing import List

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from src.Character import Character
from src.Curve import Curve
from src.Drawer import Drawer
from src.Point import Point
from src.Polygon import Polygon
from src.Train import Train

flagDrawAxis = False
scene = None
curves: List[Curve] = []
characters: List[Character] = []
player: Character = Character(model=Train(1, 0, 1), scale=Point(.5, .5, 1), isPlayer=True)


def initCurves() -> None:
    global curves

    points = []
    with open("./assets/t1.txt") as f:
        for line in f:
            coord = list(map(float, line.split()))
            points.append(Point(*coord))

    refs = []
    with open("./assets/t2.txt") as f:
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
            Path = namedtuple("Path", "curve invert")
            if ref[0] == ref2[0]:
                curve.lowNeighbours.append(Path(curve2, 1))
            if ref[0] == ref2[1]:
                curve.lowNeighbours.append(Path(curve2, 0))
            if ref[1] == ref2[0]:
                curve.upNeighbours.append(Path(curve2, 0))
            if ref[1] == ref2[1]:
                curve.upNeighbours.append(Path(curve2, 1))


def initCharacters() -> None:
    global characters

    characters.append(player)
    player.trail = curves[0]

    for _ in range(0):
        enemy = Character(model=Train(0, 1, 1),
                          scale=Point(.5, .5, 1),
                          velocity=uniform(2.0, 4.0),
                          t=.5)
        characters.append(enemy)
        enemy.trail = choice(curves[1:])
        enemy.direction = getrandbits(1)


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

    player.trail.color = 1, 0, 1
    if player.nextTrail is not None:
        player.nextTrail.curve.color = 1, 1, 0

    if flagDrawAxis:
        Drawer.drawAxis(scene)

    for curve in curves:
        curve.generate()

    for char in characters:
        char.draw()

    glutSwapBuffers()


diffEt = 0


def animate():
    global diffEt
    et = glutGet(GLUT_ELAPSED_TIME)

    for char in characters:
        char.animate(et - diffEt)

    diffEt = et

    glutPostRedisplay()


def keyboard(key: bytes, x, y) -> None:
    if key == b'q' or key == b'\x1b':
        os._exit(0)
    if key == b' ':
        player.invertDirection()

    glutPostRedisplay()


def arrow_keys(a_keys: int, x, y) -> None:
    if a_keys == GLUT_KEY_LEFT:
        player.setNext(1)
    if a_keys == GLUT_KEY_RIGHT:
        player.setNext(-1)

    glutPostRedisplay()


def main() -> None:
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(900, 900)

    glutCreateWindow("Curved Labyrinth")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    init()

    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(arrow_keys)

    # try:
    glutMainLoop()
    # except SystemExit:
    #     pass


if __name__ == '__main__':
    main()
