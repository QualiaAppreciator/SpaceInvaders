import stddraw as s
import functions as f
import math, time
from picture import Picture
from gameObjects import Enemies, Missiles, Player


BACKGROUND = Picture("background.PNG")
ENEMIES = []
MISSILES = []
ENEMY_SPEED = 1


def main():
    f.setCanvas()
    overall = True
    PLAYER_GRAPHIC = Picture("player1.PNG")

    while overall:
        menu = True
        gamePlay = True

        while menu:
            f.drawMenu()
            key = s.getKeysPressed()
            if key[s.K_p]:
                menu = False
            if key[s.K_q]:
                overall = False
                menu = False
                gamePlay = False
            if key[s.K_i]:
                f.drawInstructions()
            if key[s.K_c]:
                PLAYER_GRAPHIC = f.playerChoice()

        f.populateENEMIES(ENEMIES)
        player = Player(0,25, math.pi/2, PLAYER_GRAPHIC)
        fire_rate = 0
        score = 0
        levelCount = 1
        if gamePlay:
            levelCount = f.levelDisplay(levelCount)

        while gamePlay:
            key = s.getKeysPressed()
            s.clear()
            s.picture(BACKGROUND)
            f.score(score)

            for k in ENEMIES:
                k.draw()
                k.move()
            for j in MISSILES:
                j.draw()
                j.move()
            player.draw()
            player.drawCannon()  

            if key[s.K_a]:
                player.move('left')
            if key[s.K_d]:
                player.move('right')
            if key[s.K_j]:
                player.moveCannon('j')
            if key[s.K_l]:
                player.moveCannon('l')
            if key[s.K_SPACE] and (time.time() - fire_rate > .6):
                MISSILES.append(Missiles(player._x, player._y, player._theta))
                fire_rate = time.time()
            if key[s.K_q]:
                overall = False
                gamePlay = False
            if key[s.K_e]:
                gamePlay = False

            score = f.checkForHits(ENEMIES, MISSILES, score)

            gameStatus = f.gameStatus(ENEMIES, player)
            if gameStatus == 'YOU LOSE' or (gameStatus == 'YOU WIN' and levelCount == 4):
                gamePlay = False
            if gameStatus == 'YOU WIN' and levelCount < 4:
                levelCount = f.levelDisplay(levelCount)
                ENEMIES.clear()
                MISSILES.clear()
                f.populateENEMIES(ENEMIES)
            
            s.show(0)

        ENEMIES.clear()
        MISSILES.clear()
        if overall and not key[s.K_e]:
            f.gameOver(gameStatus)



if __name__ == '__main__': main()
