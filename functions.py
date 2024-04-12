import sys
import stdio
import stddraw as s
import math
import time
from project_main import ENEMY_SPEED, ENEMIES, MISSILES, RADIUS, LAST_MISSILE_FIRED_TIME, BACKGROUND



SPEED = .5
ANGULAR_SPEED = 0.01
MISSILE_SPEED = 0.2


# added by JOSH in project_main, moved to functions by Mikael
def drawMenu():
    s.clear(s.GRAY)
    s.picture(BACKGROUND)
    s.text(0,250,"Press p to play")
    s.text(0,238,"Press i for instructions")
    s.text(0,226,"Press e to come back")
    s.text(0,214,"Press q to quit")
    s.show(1)
    
# instructions menu accesed from the main menu
# added by JOSH                                                                          
def drawInstructions():
    instructions = True 
    while instructions:
        s.clear(s.GRAY)
        Quit = s.getKeysPressed()
        if Quit[s.K_b]:
            instructions = False
        s.picture(BACKGROUND)
        s.text(0,275,"To move left press: ' a '")
        s.text(0,260,"To move right press: ' d '")
        s.text(0,245,"To shift the canon angle left press: ' j '")
        s.text(0,230,"To shift the canon angle right press: ' l '")
        s.text(0,215,"To shoot press: SPACE BAR")
        s.text(0,200,"Press ' b ' to return to the main menu")
        s.show(1)
        
# moves player left when 'a' is pressed and right when 'd' is pressed
# added by josh
def movePlayer(keyTyped, RX):
   
    if keyTyped == 'a' or keyTyped == 'A':
        # ensures player does not cross left boarder
        if RX-RADIUS == -250:
            RX = RX
        else:
            RX -= SPEED

    if keyTyped == 'd' or keyTyped == 'D':
        # ensures player does not cross right boarder 
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
    direction_changed = False

    #Switches direction of enemy movement and moves them down when touching a border
    for m in range(15):
        if ((ENEMIES[m][0]-RADIUS <= -250) or (ENEMIES[m][0]+RADIUS >= 250)) and (ENEMIES[m][2] == 1):
            if not direction_changed:
                ENEMY_SPEED *= -1
            direction_changed = True
            for n in range(15):
                ENEMIES[n][1] -= 14

    #Checks status of enemies, draws them if alive, kills them if in contact with a missile.
    #Moves enemies horizontally
    for j in range(15):
        x = ENEMIES[j][0]
        y = ENEMIES[j][1]

        #Enemies have square hitboxes at the moment, dunno if that matters too much. Can maybe change their shape later on so that it is less obvious.
        k = 0
        while k < len(MISSILES):
            if (MISSILES[k][0] > x-RADIUS and MISSILES[k][0] < x+RADIUS) and (MISSILES[k][1] > y-RADIUS and MISSILES[k][1] < y+RADIUS) and (ENEMIES[j][2] == 1):
                ENEMIES[j][2] = 0
                del MISSILES[k]
                if ENEMY_SPEED > 0:
                    ENEMY_SPEED += 0.03
                else:
                    ENEMY_SPEED -= 0.03
            else:
                k += 1

        ENEMIES[j][0] -= ENEMY_SPEED
        
        if ENEMIES[j][2] == 1:
            s.filledCircle(ENEMIES[j][0],ENEMIES[j][1],RADIUS)


# shifts canon angle left and right 
# added by josh
def cannonAngle(keyTyped,RX,theta):
    if keyTyped == 'l':
        theta += ANGULAR_SPEED
        # ensures canon does not go past the horizontal on the left
        if theta >= math.pi:
            theta = math.pi
    if keyTyped == 'j':
        theta -= ANGULAR_SPEED
        # ensures canon does not go past the horizontal on the right 
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

    #Creates new missile when SPACE is pressed with a time interval of one second.
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
        #This if equation can be simplified, I left it like this to show my reasoning,
        #because there are some bugs with the end-game conditions.
        if (ENEMIES[i][1]-RADIUS <= 40 and ((ENEMIES[i][0]-RADIUS <= RX+RADIUS and ENEMIES[i][0]-RADIUS >= RX-RADIUS)\
             or (ENEMIES[i][0]+RADIUS <= RX+RADIUS and ENEMIES[i][0]+RADIUS >= RX-RADIUS)))\
             or ENEMIES[i][1]-RADIUS <= 0:
            return "Lost"
        living_enemies += ENEMIES[i][2]
    
    if living_enemies == 0:
        return "Won" 
    else:
        return "Continue"
