import sys
import stdio
import stddraw as s
import stdarray
import math

RADIUS = 20
SPEED = .5
ANGULAR_SPEED = 0.01
MISSILE_SPEED = 0.02

def movePlayer(keyTyped, RX):
   
    if keyTyped == 'a' or keyTyped == 'A':
        if RX-RADIUS == -250:
            RX = RX
        else:
            RX = RX - SPEED

    if keyTyped == 'd' or keyTyped == 'D':
        if RX+RADIUS == 250:
            RX = RX
        else:
            RX = RX + SPEED

    return RX

def enemies(ENEMIES_HEALTH):
    s.setPenColor(s.RED)
    y = 450
    for i in range(3):
        x =  -100
        for j in range(5):
            if ENEMIES_HEALTH[i][j] != 0:
                s.filledCircle(x,y,RADIUS)
                x += 50
        y -= 50

def cannonAngle(keyTyped,RX,theta):
    if keyTyped == 'l':
        theta += ANGULAR_SPEED
        if theta >= math.pi:
            theta = math.pi
    if keyTyped == 'j':
        theta -= ANGULAR_SPEED
        if theta <= 0:
            theta = 0
    return theta

def drawCannon(RX,theta):
    s.setPenColor(s.BLUE)
    s.setPenRadius(2.5)
    if theta <= math.pi/2:
        s.line(RX,20,RX-RADIUS*math.cos(theta),20+RADIUS*math.sin(theta))
    else:
        s.line(RX,20,RX+RADIUS*math.sin(theta-math.pi/2),20+RADIUS*math.cos(theta-math.pi/2))

def missile(RX, theta, MISSILES, keyTyped):
    s.setPenColor(s.WHITE)

    if keyTyped == ' ':
        MISSILES.append([RX, 20, theta])

    i = 1
    while i < len(MISSILES):
        if MISSILES[i][2] <= math.pi/2:
            MISSILES[i][0] -= MISSILE_SPEED*RADIUS*math.cos(MISSILES[i][2])
        else:
            MISSILES[i][0] -= MISSILE_SPEED*RADIUS*math.cos(MISSILES[i][2])
        MISSILES[i][1] += MISSILE_SPEED*RADIUS*math.sin(MISSILES[i][2])

        s.filledCircle(MISSILES[i][0], MISSILES[i][1], 3)
        i += 1


