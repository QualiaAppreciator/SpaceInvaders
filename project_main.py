import stddraw as s
import stdio
import functions as f
import random
import time 
import math
from picture import Picture
######################################################################
# GLOBAL VARIABLES DECLARED HERE 
RADIUS = 20
ENEMIES = []
MISSILES = []
ENEMY_SPEED = 0.08
HIGHSCORE = 0
LAST_MISSILE_FIRED_TIME = -1
BACKGROUND = Picture('background.PNG')
#####################################################################

def main():

    s.setCanvasSize(500,500)
    s.setXscale(-250,250)
    s.setYscale(0,500)

    menu = True
    overall = True

    f.createEnemies()

    while overall == True:

        menu = True
        rx = 0.0
        s.setPenColor(s.BLACK)

        while menu == True:
            f.drawMenu()

            key = s.getKeysPressed()

            if key[s.K_p]:
                menu = False
            elif key[s.K_q]:
                overall = False
                menu = False
            elif key[s.K_i]: #instructions option
                f.drawInstructions()

        if overall == False:
            game_play = False
        else:
            game_play = True

        theta = math.pi/2

        while game_play == True:
            key = ''

            key = s.getKeysPressed()

            if key[s.K_e]:
                game_play = False
            elif key[s.K_q]:
                overall = False
                game_play = False
            elif key[s.K_a]:
                key = 'a'
            elif key[s.K_d]:
                key = 'd'
            elif key[s.K_j]:
                key = 'j'
            elif key[s.K_l]:
                key = 'l'
            elif key[s.K_SPACE]:
                key = ' '
 
            rx = f.movePlayer(key,rx)  
            theta = f.cannonAngle(key,rx,theta)
            
            s.clear(s.BLACK)
            s.picture(BACKGROUND)
            f.moveEnemies()
            s.setPenColor(s.GREEN)
            s.filledCircle(rx,20,RADIUS)
            f.drawCannon(rx,theta)
            f.missile(rx,theta,key)

            gameStatus = f.checkGameStatus(rx)
            if gameStatus == "Lost" or gameStatus == "Won":
                overall = False
                game_play = False

            s.show(1)


    s.clear(s.BLACK)
    s.setPenColor(s.WHITE)
    s.text(0,250,"Thanks for playing")
    s.show()

if __name__ == '__main__': main()
