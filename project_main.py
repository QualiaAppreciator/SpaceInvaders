import stddraw as s
import stdio
import functions as f
import random
import time 
import math

######################################################################
# GLOBAL VARIABLES DECLARED HERE 
RADIUS = 20
ENEMIES = []
MISSILES = []
ENEMY_SPEED = 0.15
######################################################################

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
            s.clear(s.WHITE)
            s.text(0,250,"Press p to play")
            s.text(0,238,"Press e to come back")
            s.text(0,226,"Press q to quit")
            s.show(1)

            key = s.getKeysPressed()

            if key[s.K_p]:
                menu = False
            elif key[s.K_q]:
                overall = False
                menu = False

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
            
            f.moveEnemies()
            s.setPenColor(s.GREEN)
            s.filledCircle(rx,20,RADIUS)
            f.drawCannon(rx,theta)
            f.missile(rx,theta,key)
            s.show(1)

    s.clear(s.BLACK)
    s.setPenColor(s.WHITE)
    s.text(0,250,"Thanks for playing")
    s.show(0)
    time.sleep(3)

if __name__ == '__main__': main()
