# -*- coding: utf-8 -*-
import argparse
from audioop import maxpp
import os
from random import choice, getrandbits, uniform
from typing import List

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import src.helpers.settings as settings
from src.helpers.Drawer import Drawer
from src.models.Character import Character
from src.models.Curve import Curve
from src.models.Point import Point
from src.models.Polygon import Polygon

NUM_OF_ENEMIES = 10

scene: Polygon = None
curves: List[Curve] = []
characters: List[Character] = []
player: Character = Character(
    model=Polygon(
        filepath="assets/models/player.txt",
        color=[1, 0, 0]
    ),
    scale=Point(.15, .15, 1)
)

diffEt = 0
lastTime = 0
framesPerSecond = 0
displayFPS = 1
pause = True


def initCurves() -> None:
    global curves

    refs = []
    with open("./assets/curve/curves.txt") as f:
        for line in f:
            curves.append(Curve([scene[i] for i in map(int, line.split())]))
            refs.append(line.split())

    for ref, looking in zip(refs, curves):
        for ref2, neighbour in zip(refs, curves):
            if looking is neighbour:
                continue
            if ref[0] == ref2[0]:
                looking.startNeighbours.append((neighbour, False))
            if ref[0] == ref2[2]:
                looking.startNeighbours.append((neighbour, True))
            if ref[2] == ref2[0]:
                looking.endNeighbours.append((neighbour, True))
            if ref[2] == ref2[2]:
                looking.endNeighbours.append((neighbour, False))


def initCharacters() -> None:
    global characters
    characters.clear()

    characters.append(player)
    player.trail = curves[0]

    for _ in range(NUM_OF_ENEMIES):
        characters.append(
            Character(
                model=Polygon(
                    filepath="assets/models/enemy.txt"
                ),
                scale=Point(.15, .15, 1),
                velocity=uniform(1.0, 2.0),
                sense=getrandbits(1),
                trail=choice(curves[1:]),
                t=.5)
        )


def init() -> None:
    global scene

    with open("./assets/curve/points.txt") as f:
        scene = Polygon(
            vertices=[Point(*(map(float, line.split()))) for line in f]
        )
    initCurves()
    initCharacters()


def reshape(w, h):
    minPoint, maxPoint = scene.getLimits()

    glViewport(int(minPoint.x), int(minPoint.y), w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(minPoint.x, maxPoint.x,
            minPoint.y, maxPoint.y, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def display() -> None:
    global lastTime, framesPerSecond, displayFPS, pause
    glClearColor(.0, .0, .0, .0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    currentTime = glutGet(GLUT_ELAPSED_TIME) * .001
    framesPerSecond += 1
    if currentTime - lastTime > 1.:
        lastTime = currentTime
        displayFPS = framesPerSecond
        framesPerSecond = 0
    sceneMin, sceneMax = scene.getLimits()
    if settings._debugger:
        Drawer.displayTitle(f"FPS: {displayFPS}", sceneMin.x+.3, sceneMax.y-.3)
        Drawer.drawAxis(scene)

    if pause:
        Drawer.displayTitle(f"Pause", sceneMax.x-.8, sceneMax.y-.3)

    player.trail.color = .5, 1, .5
    player.trail.width = 2
    if player.nextTrail is not None:
        player.nextTrail[0].color = .5, .5, 1
        player.nextTrail[0].width = 4

    for curve in curves:
        curve.generate()

    player.display()

    for char in characters[1:]:
        char.display()
        if player.collided(char):
            pause = True
            Drawer.displayTitle(f"You lost ):", (sceneMax.x +
                                sceneMin.x) / 2 - .55, sceneMax.y - .3)

    glutSwapBuffers()


def animate():
    global diffEt
    et = glutGet(GLUT_ELAPSED_TIME) * .0005

    for char in characters:
        char.animate((et - diffEt) * (not pause))

    diffEt = et

    glutPostRedisplay()


def keyboard(key: bytes, x, y) -> None:
    if key == b'q' or key == b'\x1b':
        os._exit(0)
    if key == b'b':
        player.invertDirection()
    if key == b' ':
        player.handbreak = not player.handbreak
    if key == b'p':
        global pause
        pause = not pause
    if key == b']':
        player.trail.steps += 1
    if key == b'[':
        player.trail.steps -= 1

    glutPostRedisplay()


def arrow_keys(a_keys: int, x, y) -> None:
    if a_keys == GLUT_KEY_LEFT:
        player.setNext(1)
    if a_keys == GLUT_KEY_RIGHT:
        player.setNext(-1)

    glutPostRedisplay()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug', action=argparse.BooleanOptionalAction, default=False)
    args = parser.parse_args()

    settings.init(args.debug)

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(900, 900)

    glutCreateWindow("Curved Labyrinth")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    init()
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(arrow_keys)

    try:
        glutMainLoop()
    except SystemExit:
        pass


if __name__ == '__main__':
    main()
