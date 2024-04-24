import stddraw as s
import functions as f
import math, time
from picture import Picture
from gameObjects import Enemies, Missiles, Player

BACKGROUND = Picture("background.PNG")
ENEMIES = []
MISSILES = []
ENEMY_MISSILES = []
BUNKERS = []
MISSILES2 = []


def main():
    f.setCanvas()
    overall = True
    PLAYER_GRAPHIC = Picture("player1.PNG")

    while overall:
        menu = True
        gamePlay = True
        twoPlayers = False

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
            if key[s.K_o]:
                twoPlayers = True
                menu = False

        f.populateENEMIES(ENEMIES)
        f.populateBUNKERS(BUNKERS)
        player = Player(0,25, math.pi/2, PLAYER_GRAPHIC,1)
        player_last_fired = 0
        if twoPlayers:
            player2 = Player(125,25,math.pi/2,PLAYER_GRAPHIC,1)
            player2_last_fired = 0
            player._x = -125
        score = 0
        levelCount = 1
        if gamePlay:
            levelCount = f.levelDisplay(levelCount)

        while gamePlay:
            key = s.getKeysPressed()
            s.clear()
            s.picture(BACKGROUND)
            f.score(score)
            gameStatus = f.gameStatus(ENEMIES, ENEMY_MISSILES)
            player._hitpoints = f.checkIfPlayerHit(player, ENEMY_MISSILES, ENEMIES)

            for k in ENEMIES:
                k.draw()
                k.move()
            for j in MISSILES:
                j.draw()
                j.move()
            for g in ENEMY_MISSILES:
                g.draw()
                g.move()
            for p in BUNKERS:
                p.draw()
            player.draw()
            player.drawCannon()  

            if key[s.K_a]:
                player.move('left')
            if key[s.K_d]:
                player.move('right')
            if key[s.K_4]:
                player.moveCannon('j')
            if key[s.K_6]:
                player.moveCannon('l')
            if key[s.K_SPACE] and (time.time() - player_last_fired > .6) and player._hitpoints > 0:
                MISSILES.append(Missiles(player._x, player._y, player._theta, 0))
                player_last_fired = time.time()

# everthing below 'if twoPlayers' will run if twoPlayers is true, this will implement multiplayer mode
            if twoPlayers:
                for i in MISSILES2:
                    i.draw()
                    i.move()
                player2.draw()
                player2.drawCannon()
                if key[s.K_j]:
                    player2.move('left')
                if key[s.K_l]:
                    player2.move('right')
                if key[s.K_b]:
                    player2.moveCannon('left')
                if key[s.K_m]:
                    player2.moveCannon('right')
                if key[s.K_u] and (time.time() - player2_last_fired > .6) and player2._hitpoints > 0:
                    MISSILES2.append(Missiles(player2._x, player2._y, player2._theta, 0))
                    player2_last_fired = time.time()

                f.enemyCounterattack(player2, ENEMY_MISSILES, ENEMIES)
                score = f.checkForHits(ENEMIES, BUNKERS, MISSILES2, score)

                if player2._hitpoints > 0:
                    player2._hitpoints = f.checkIfPlayerHit(player2, ENEMY_MISSILES, ENEMIES)

                if (player._hitpoints <= 0 and player2._hitpoints <= 0) or (gameStatus == 'WON' and levelCount == 4):
                    gamePlay = False
                    
                if gameStatus == 'WON' and levelCount < 4:
                    levelCount = f.levelDisplay(levelCount)
                    ENEMIES.clear()
                    MISSILES.clear()
                    MISSILES2.clear()
                    ENEMY_MISSILES.clear()
                    f.populateENEMIES(ENEMIES)
                    player = Player(-125,25, math.pi/2, PLAYER_GRAPHIC,1)
                    player2 = Player(125,25,math.pi/2,PLAYER_GRAPHIC,1)

            if key[s.K_q]:
                overall = False
                gamePlay = False
            if key[s.K_e]:
                gamePlay = False

            score = f.checkForHits(ENEMIES, BUNKERS, MISSILES, score)
            #if levelCount > 2:
            f.enemyCounterattack(player, ENEMY_MISSILES, ENEMIES)

            if (player._hitpoints <= 0 and twoPlayers == False) or (gameStatus == 'WON' and levelCount == 4):
                gamePlay = False
            if gameStatus == 'WON' and levelCount < 4 and twoPlayers == False:
                levelCount = f.levelDisplay(levelCount)
                ENEMIES.clear()
                MISSILES.clear()
                ENEMY_MISSILES.clear()
                f.populateENEMIES(ENEMIES)
            
            s.show(0)

        ENEMIES.clear()
        MISSILES.clear()
        MISSILES2.clear()
        ENEMY_MISSILES.clear()
        if overall and not key[s.K_e]:
            f.gameOver(levelCount, score)



if __name__ == '__main__': main()
