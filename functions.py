import sys
import stdio
import stddraw as s
import math
import time
from project_main import ENEMY_SPEED, ENEMIES, MISSILES, RADIUS, LAST_MISSILE_FIRED_TIME



SPEED = .5
ANGULAR_SPEED = 0.01
MISSILE_SPEED = 0.2



def movePlayer(keyTyped, RX):
   
    if keyTyped == 'a' or keyTyped == 'A':
        if RX-RADIUS == -250:
            RX = RX
        else:
            RX -= SPEED

    if keyTyped == 'd' or keyTyped == 'D':
        if RX+RADIUS == 250:
            RX = RX
        else:
            RX += SPEED

    return RX



#Changed ENEMIES to a nested list, where each nested list is one enemy -> [x, y, health status]
#Creates enemies once off in their starting positions
def createEnemies():
    y = 450
    for i in range(3):
        x =  -100
        for j in range(5):
            ENEMIES.append([x,y,1])
            x += 50
        y -= 50



#Added by Mikael
def moveEnemies():
    global ENEMY_SPEED
    s.setPenColor(s.RED)

    #Switches direction of enemy movement and moves them down when touching a border
    for m in range(15):
        if ((ENEMIES[m][0]-RADIUS <= -250) or (ENEMIES[m][0]+RADIUS >= 250)) and (ENEMIES[m][2] == 1):
            for n in range(15):
                ENEMIES[n][1] -= 12
            ENEMY_SPEED *= -1

    #Checks status of enemies, draws them if alive, kills them if in contact with a missile.
    #Moves enemies horizontally
    for j in range(15):
        x = ENEMIES[j][0]
        y = ENEMIES[j][1]

        #Enemies have square hitboxes at the moment, dunno if that matters too much. Can maybe change their shape later on so that it is less obvious.
        k = 1
        while k < len(MISSILES):
            if (MISSILES[k][0] > x-RADIUS and MISSILES[k][0] < x+RADIUS) and (MISSILES[k][1] > y-RADIUS and MISSILES[k][1] < y+RADIUS) and (ENEMIES[j][2] == 1):
                ENEMIES[j][2] = 0
                del MISSILES[k]
            else:
                k += 1

        ENEMIES[j][0] -= ENEMY_SPEED
        
        if ENEMIES[j][2] == 1:
            s.filledCircle(ENEMIES[j][0],ENEMIES[j][1],RADIUS)



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



#Added by Mikael
def missile(RX, theta, keyTyped):
    global LAST_MISSILE_FIRED_TIME
    s.setPenColor(s.WHITE)

    #Creates new missile when SPACE is pressed.       
    CURRENT_TIME = time.time()
    if keyTyped == ' ' and CURRENT_TIME - LAST_MISSILE_FIRED_TIME >= 1:
        MISSILES.append([RX, 20, theta])
        LAST_MISSILE_FIRED_TIME = time.time()

    #Moves all missiles forward on their trajectory by one frame.
    #Deletes a missiles if it goes out of bounds
    i = 0
    while i < len(MISSILES):
        if MISSILES[i][2] <= math.pi/2:
            MISSILES[i][0] -= MISSILE_SPEED*math.cos(MISSILES[i][2])
        else:
            MISSILES[i][0] -= MISSILE_SPEED*math.cos(MISSILES[i][2])
        MISSILES[i][1] += MISSILE_SPEED*math.sin(MISSILES[i][2])

        if MISSILES[i][0] > 250 or MISSILES[i][0] < -250 or MISSILES[i][1] > 500:
            del MISSILES[i]
        else:
            s.filledCircle(MISSILES[i][0], MISSILES[i][1], 3)
            i += 1



#Added by Mikael
#Returns "Lost" if enemies touch the turret or the bottom border
#Returns "Won" if all enemies have been killed
def checkGameStatus(RX):
    living_enemies = 0
    
    for i in range(15):
        if (ENEMIES[i][1]-RADIUS <= 40 and ((ENEMIES[i][0]-RADIUS <= RX+RADIUS and ENEMIES[i][0]-RADIUS >= RX-RADIUS)\
             or (ENEMIES[i][0]+RADIUS <= RX+RADIUS and ENEMIES[i][0]+RADIUS >= RX-RADIUS)))\
             or ENEMIES[i][1]-RADIUS <= 0:
            return "Lost"
        living_enemies += ENEMIES[i][2]
    
    if living_enemies == 0:
        return "Won" 
    else:
        return "Continue"