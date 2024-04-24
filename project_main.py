import stddraw as s
import stdaudio
import functions as f
import math, time
from picture import Picture
from gameObjects import Enemies, Missiles, Player
from threading import Thread


BACKGROUND = Picture("background.PNG")
ENEMIES = []
MISSILES = []
ENEMY_MISSILES = []
BUNKERS = []


def main():
    f.setCanvas()
    overall = True
    PLAYER_GRAPHIC = Picture("player1.PNG")

    music_thread = Thread(target=f.music,daemon=True)
    music_thread.start()

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
        f.populateBUNKERS(BUNKERS)
        player = Player(0,25, math.pi/2, PLAYER_GRAPHIC)
        player_last_fired = 0
        score = 0
        levelCount = 1
        if gamePlay:
            levelCount = f.levelDisplay(levelCount)

        while gamePlay:
            key = s.getKeysPressed()
            s.clear()
            s.picture(BACKGROUND)
            f.score()

            f.moveEverything(ENEMIES, MISSILES, ENEMY_MISSILES, BUNKERS, player)
            f.checkForHits(ENEMIES, BUNKERS, MISSILES)

            if key[s.K_a]:
                player.move('left')
            if key[s.K_d]:
                player.move('right')
            if key[s.K_j]:
                player.moveCannon('j')
            if key[s.K_l]:
                player.moveCannon('l')
            if key[s.K_SPACE] and (time.time() - player_last_fired > .6):
                MISSILES.append(Missiles(player._x, player._y, player._theta, 0))
                # pew_thread = Thread(target=f.pew,daemon=True)
                # pew_thread.start()
                player_last_fired = time.time()
            if key[s.K_q]:
                overall = False
                gamePlay = False
            if key[s.K_e]:
                gamePlay = False

            #if levelCount > 2:
            f.enemyCounterattack(player._x, ENEMY_MISSILES, ENEMIES)

            gameStatus = f.gameStatus(ENEMIES, player, ENEMY_MISSILES)
            if gameStatus == 'LOST' or (gameStatus == 'WON' and levelCount == 4):
                gamePlay = False
            if gameStatus == 'WON' and levelCount < 4:
                levelCount = f.levelDisplay(levelCount)
                ENEMIES.clear()
                MISSILES.clear()
                ENEMY_MISSILES.clear()
                f.populateENEMIES(ENEMIES)
            
            s.show(0)

        ENEMIES.clear()
        MISSILES.clear()
        ENEMY_MISSILES.clear()
        if overall and not key[s.K_e]:
            f.gameOver(levelCount, score)


if __name__ == '__main__': main()
