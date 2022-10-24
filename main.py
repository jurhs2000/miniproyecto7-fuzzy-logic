# Universidad del Valle de Guatemala
# CC3039 - Modelacion & Simulacion
# Miniproyecto 7 - Logica Difusa
# Julio Herrera - 19402
# Diego Arredondo - 19422
# Oscar Saravia - 19122

from textwrap import fill
from unicodedata import name
import numpy as np
import random
import cv2

WIDTH = 800
HEIGHT = 800
FONT = cv2.FONT_HERSHEY_DUPLEX
SIZE = 0.7
WHITE = (1, 1, 1)
BLACK = (0, 0, 0)
GREEN = (0, 1, 0)
RED = (0, 0, 1)
GRASS = (39/255, 168/255, 13/255)
RED = (0, 0, 1)
GOALPT1 = (WIDTH-20, 300)
GOALPT2 = (WIDTH, 500)

def drawCamp():
    # dibujar la cancha
    frame = np.ones((HEIGHT, WIDTH, 3))
    frame *= GRASS
    cv2.rectangle(frame, pt1=(400, 150), pt2=(WIDTH+3, 650), color=WHITE, thickness=5)
    cv2.rectangle(frame, pt1=GOALPT1, pt2=GOALPT2, color=WHITE, thickness=-1)
    cv2.circle(frame, center=(400, 400), radius=20, color=WHITE, thickness=-1)
    return frame

def drawBall(frame, state):
    cv2.circle(frame, center=(state['ball']['x'], state['ball']['y']), radius=10, color=RED, thickness=-1)
    return frame

def drawPlayer(frame, state):
    cv2.rectangle(frame, pt1=(state['player']['x'], state['player']['y']), pt2=(state['player']['x']+20, state['player']['y']+20), color=BLACK, thickness=-1)
    return frame

# Función para dibujar el estado de la simulación
def draw(state):
    frame = drawCamp()
    frame = drawBall(frame, state)
    frame = drawPlayer(frame, state)
    cv2.imshow("Fuzzy Logic", frame)
    cv2.waitKey(5)

def fuzzyLogic(state):
    plotFunctions = False
    if state is None:
        # definir estado inicial
        state = {
            "ball": {
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "vx": random.randint(0, 0),
                "vy": random.randint(0, 0)
            },
            "player": {
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT)
            }
        }
        plotFunctions = True
    #
    return state

if __name__ == "__main__":
    state = None
    while True:
        state = fuzzyLogic(state)
        draw(state)