# Universidad del Valle de Guatemala
# CC3039 - Modelacion & Simulacion
# Miniproyecto 7 - Logica Difusa
# Julio Herrera - 19402
# Diego Arredondo - 19422
# Oscar Saravia - 19122

from cmath import acos
from turtle import distance
import numpy as np
import random
import math
import cv2
import matplotlib.pyplot as plt

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
    cv2.circle(frame, center=(int(state['ball']['x']), int(state['ball']['y'])), radius=10, color=RED, thickness=-1)
    return frame

def drawPlayer(frame, state):
    cv2.rectangle(frame, pt1=(state['player']['x'], state['player']['y']), pt2=(state['player']['x']+20, state['player']['y']+20), color=BLACK, thickness=-1)
    return frame

# Función para dibujar el estado de la simulación
def draw(state):
    frame = drawCamp()
    frame = drawBall(frame, state)
    frame = drawPlayer(frame, state)
    cv2.putText(frame, "Iterations: " + str(state['iterations']), (10, 30), FONT, SIZE, WHITE)
    cv2.imshow("Fuzzy Logic", frame)
    cv2.waitKey(1)

maxDistance = math.sqrt(WIDTH**2 + HEIGHT**2)
# Based on WIDTH and HEIGHT of the window
DISTANCEINPUT = {
    "close": [{"distance": 1, "membership": 1}, {"distance": maxDistance/4, "membership": 1}, {"distance": maxDistance/3, "membership": 0.2}, {"distance": (maxDistance/2)*0.8, "membership": 0}],
    "medium": [{"distance": (maxDistance/3)*0.75, "membership": 0}, {"distance": maxDistance/2, "membership": 1}, {"distance": (maxDistance/3)*2, "membership": 0.4}, {"distance": (maxDistance/3)*2*1.2, "membership": 0}],
    "far": [{"distance": (maxDistance/2)*1.2, "membership": 0}, {"distance": (maxDistance/3)*2, "membership": 0.2}, {"distance": maxDistance, "membership": 1}]
}
FORCEINPUT = {
    "low": [{"proximity": "close", "membership": 1}, {"proximity": "medium", "membership": 0.25}, {"proximity": "far", "membership": 0}],
    "medium": [{"proximity": "close", "membership": 0.1}, {"proximity": "medium", "membership": 1}, {"proximity": "far", "membership": 0.4}],
    "high": [{"proximity": "close", "membership": 0}, {"proximity": "medium", "membership": 0.75}, {"proximity": "far", "membership": 1}]
}
ANGLEINPUT = {
    "little": [{"angle": 0, "membership": 1}, {"angle": 22, "membership": 0.5}, {"angle": 45, "membership": 0}],
    "medium": [{"angle": 30, "membership": 0}, {"angle": 45, "membership": 1}, {"angle": 60, "membership": 0}],
    "much": [{"angle": 50, "membership": 0}, {"angle": 80, "membership": 0.8}, {"angle": 90, "membership": 1}]
}

def plotFuzzyFunctions():
    plt.figure()
    plt.title("Reach Ball")
    plt.ylabel("Membership")
    plt.xlabel("Distance")
    for key in DISTANCEINPUT:
        plt.plot([point['distance'] for point in DISTANCEINPUT[key]], [point['membership'] for point in DISTANCEINPUT[key]], label=key)
    plt.legend()
    plt.show()
    # plot force
    plt.figure()
    plt.title("Force")
    plt.ylabel("Membership")
    plt.xlabel("Proximity")
    for key in FORCEINPUT:
        plt.plot([point['proximity'] for point in FORCEINPUT[key]], [point['membership'] for point in FORCEINPUT[key]], label=key)
    plt.legend()
    plt.show()
    # plot angle
    plt.figure()
    plt.title("Angle")
    plt.ylabel("Membership")
    plt.xlabel("Angle")
    for key in ANGLEINPUT:
        plt.plot([point['angle'] for point in ANGLEINPUT[key]], [point['membership'] for point in ANGLEINPUT[key]], label=key)
    plt.legend()
    plt.show()

def getDistanceMembership(distance):
    membership = {
        "close": 0,
        "medium": 0,
        "far": 0
    }
    for key in DISTANCEINPUT:
        for iPoint in range(len(DISTANCEINPUT[key])):
            if distance == DISTANCEINPUT[key][iPoint]['distance']:
                membership[key] = DISTANCEINPUT[key][iPoint]['membership']
                break
            if iPoint == len(DISTANCEINPUT[key])-1 and distance > DISTANCEINPUT[key][iPoint]['distance']:
                membership[key] = 0
                break
            elif distance > DISTANCEINPUT[key][iPoint]['distance'] and distance < DISTANCEINPUT[key][iPoint+1]['distance']:
                v1Points = [(DISTANCEINPUT[key][iPoint]['distance'], DISTANCEINPUT[key][iPoint]['membership']), (DISTANCEINPUT[key][iPoint+1]['distance'],DISTANCEINPUT[key][iPoint]['membership'])]
                v2Points = [(DISTANCEINPUT[key][iPoint]['distance'], DISTANCEINPUT[key][iPoint]['membership']), (DISTANCEINPUT[key][iPoint+1]['distance'],DISTANCEINPUT[key][iPoint+1]['membership'])]
                # points to vectors
                v1 = np.array(v1Points[1]) - np.array(v1Points[0])
                v2 = np.array(v2Points[1]) - np.array(v2Points[0])
                # get angle using points of vectors
                angle = math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                # radians to degrees
                angle = math.degrees(angle)
                if angle == 0:
                    membership[key] = DISTANCEINPUT[key][iPoint]['membership']
                baseMembership = 0
                if DISTANCEINPUT[key][iPoint]['membership'] != 0 and DISTANCEINPUT[key][iPoint+1]['membership'] != 0:
                    if DISTANCEINPUT[key][iPoint]['membership'] > DISTANCEINPUT[key][iPoint+1]['membership']:
                        baseMembership = DISTANCEINPUT[key][iPoint+1]['membership']
                    else:
                        baseMembership = DISTANCEINPUT[key][iPoint]['membership']
                # get angle using points of vectors AGAIN
                angle = math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                membershipValue = ((distance - DISTANCEINPUT[key][iPoint]['distance']) * math.tan(angle))
                if DISTANCEINPUT[key][iPoint]['membership'] > DISTANCEINPUT[key][iPoint+1]['membership']:
                    membershipValue = ((DISTANCEINPUT[key][iPoint+1]['distance'] - distance) * math.tan(angle))
                membership[key] = membershipValue + baseMembership
                break
    return membership

def movePlayerToBallRules(state, distanceMembership):
    fuzzyOutput = {
        "left": 0,
        "right": 0,
        "up": 0,
        "down": 0
    }
    moveFastProbability = (distanceMembership['far'] + distanceMembership['medium'])/2
    moveSlowProbability = (distanceMembership['close'] + distanceMembership['medium'])/2
    if state['player']['x'] < state['ball']['x']:
        randomValue = random.random()
        if randomValue < moveFastProbability:
            fuzzyOutput['right'] = random.randint(1, 10)
        elif randomValue < moveSlowProbability:
            fuzzyOutput['right'] = 1
    if state['player']['x'] > state['ball']['x']:
        randomValue = random.random()
        if randomValue < moveFastProbability:
            fuzzyOutput['left'] = random.randint(1, 10)
        elif randomValue < moveSlowProbability:
            fuzzyOutput['left'] = 1
    if state['player']['y'] < state['ball']['y']:
        randomValue = random.random()
        if randomValue < moveFastProbability:
            fuzzyOutput['down'] = random.randint(1, 10)
        elif randomValue < moveSlowProbability:
            fuzzyOutput['down'] = 1
    if state['player']['y'] > state['ball']['y']:
        randomValue = random.random()
        if randomValue < moveFastProbability:
            fuzzyOutput['up'] = random.randint(1, 10)
        elif randomValue < moveSlowProbability:
            fuzzyOutput['up'] = 1
    return fuzzyOutput

def movePlayerToBall(state, fuzzyOutput):
    if fuzzyOutput['left'] > 0:
        state['player']['x'] -= fuzzyOutput['left']
    if fuzzyOutput['right'] > 0:
        state['player']['x'] += fuzzyOutput['right']
    if fuzzyOutput['up'] > 0:
        state['player']['y'] -= fuzzyOutput['up']
    if fuzzyOutput['down'] > 0:
        state['player']['y'] += fuzzyOutput['down']
    return state

def getAngleMembership(angle):
    membership = {
        "little": 0,
        "medium": 0,
        "much": 0
    }
    angle = abs(angle)
    for key in ANGLEINPUT:
        for iPoint in range(len(ANGLEINPUT[key])):
            if angle == ANGLEINPUT[key][iPoint]['angle']:
                membership[key] = ANGLEINPUT[key][iPoint]['membership']
                break
            if iPoint == len(ANGLEINPUT[key])-1 and angle > ANGLEINPUT[key][iPoint]['angle']:
                membership[key] = 0
                break
            elif angle > ANGLEINPUT[key][iPoint]['angle'] and angle < ANGLEINPUT[key][iPoint+1]['angle']:
                v1Points = [(ANGLEINPUT[key][iPoint]['angle'], ANGLEINPUT[key][iPoint]['membership']), (ANGLEINPUT[key][iPoint+1]['angle'],ANGLEINPUT[key][iPoint]['membership'])]
                v2Points = [(ANGLEINPUT[key][iPoint]['angle'], ANGLEINPUT[key][iPoint]['membership']), (ANGLEINPUT[key][iPoint+1]['angle'],ANGLEINPUT[key][iPoint+1]['membership'])]
                # points to vectors
                v1 = np.array(v1Points[1]) - np.array(v1Points[0])
                v2 = np.array(v2Points[1]) - np.array(v2Points[0])
                # get angle using points of vectors
                angleTriangle = math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                # radians to degrees
                angleTriangle = math.degrees(angleTriangle)
                if angleTriangle == 0:
                    membership[key] = ANGLEINPUT[key][iPoint]['membership']
                baseMembership = 0
                if ANGLEINPUT[key][iPoint]['membership'] != 0 and ANGLEINPUT[key][iPoint+1]['membership'] != 0:
                    if ANGLEINPUT[key][iPoint]['membership'] > ANGLEINPUT[key][iPoint+1]['membership']:
                        baseMembership = ANGLEINPUT[key][iPoint+1]['membership']
                    else:
                        baseMembership = ANGLEINPUT[key][iPoint]['membership']
                # get angle using points of vectors AGAIN
                angleTriangle = math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
                membershipValue = ((angle - ANGLEINPUT[key][iPoint]['angle']) * math.tan(angleTriangle))
                if ANGLEINPUT[key][iPoint]['membership'] > ANGLEINPUT[key][iPoint+1]['membership']:
                    membershipValue = ((ANGLEINPUT[key][iPoint+1]['angle'] - angle) * math.tan(angleTriangle))
                membership[key] = membershipValue + baseMembership
                break
    return membership

def shotRules(state, distanceMembership, angleMembership):
    print(distanceMembership, angleMembership)
    fuzzyOutput = {
        "angle": 0,
        "power": 0
    }
    inputMembership = 0
    for key in distanceMembership:
        if distanceMembership[key] > inputMembership:
            inputMembership = distanceMembership[key]
    for key in FORCEINPUT:
        for input in FORCEINPUT[key]:
            if input['proximity'] == inputMembership:
                fuzzyOutput['power'] = (input['membership'] + distanceMembership[inputMembership])/2
                break
    angleToGoal = 0
    if state['ball']['y'] < GOALPT1[1]:
        angleToGoal = math.atan((state['ball']['x'] - GOALPT1[0])/(state['ball']['y'] - GOALPT1[1]))
    elif state['ball']['y'] > GOALPT2[1]:
        angleToGoal = math.atan((state['ball']['x'] - GOALPT2[0])/(state['ball']['y'] - GOALPT2[1]))
    fuzzyOutput['angle'] = angleToGoal
    return fuzzyOutput

def shot(state, fuzzyOutput):
    state['ball']['vx'] = fuzzyOutput['power'] * math.cos(fuzzyOutput['angle'])
    state['ball']['vy'] = fuzzyOutput['power'] * math.sin(fuzzyOutput['angle'])
    state['ball']['x'] += state['ball']['vx']
    state['ball']['y'] += state['ball']['vy']
    return state

def fuzzyLogic(state):
    plotFunctions = False
    if state is None:
        # definir estado inicial, variables de entrada crisp
        state = {
            "ball": {
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "vx": random.randint(0, 0),
                "vy": random.randint(0, 0)
            },
            "player": {
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "reachBall": False
            },
            "iterations": 0
        }
        plotFunctions = True
    # fuzzification
    if plotFunctions:
        plotFuzzyFunctions()
    # Move Player to Ball
    distancePlayerBall = math.sqrt((state['ball']['x'] - state['player']['x'])**2 + (state['ball']['y'] - state['player']['y'])**2)
    membershipDistancePB = getDistanceMembership(distancePlayerBall)
    # rules
    fuzzyOutputPB = movePlayerToBallRules(state, membershipDistancePB)
    # defuzzification
    state = movePlayerToBall(state, fuzzyOutputPB)
    if state['player']['x'] == state['ball']['x'] and state['player']['y'] == state['ball']['y']:
        state['player']['reachBall'] = True
    # shot
    if state['player']['reachBall']:
        # fuzzification
        distanceBallGoal = math.sqrt((WIDTH - state['ball']['x'])**2 + (HEIGHT/2 - state['ball']['y'])**2)
        v1Points = [(state['ball']['x'], state['ball']['y']), (WIDTH, state['ball']['y'])]
        v2Points = [(state['ball']['x'], state['ball']['y']), (WIDTH, HEIGHT/2)]
        # points to vectors
        v1 = np.array(v1Points[1]) - np.array(v1Points[0])
        v2 = np.array(v2Points[1]) - np.array(v2Points[0])
        # get angle using points of vectors
        angleTriangle = math.acos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        membershipDistanceBG = getDistanceMembership(distanceBallGoal)
        membershipAngleBG = getAngleMembership(math.degrees(angleTriangle))
        # rules
        fuzzyOutputBG = shotRules(state, membershipDistanceBG, membershipAngleBG)
        # defuzzification
        state = shot(state, fuzzyOutputBG)
    state['iterations'] += 1
    return state

if __name__ == "__main__":
    state = None
    while True:
        state = fuzzyLogic(state)
        draw(state)