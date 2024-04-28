import stddraw as s
import functions as f
import math, time
from picture import Picture
from gameObjects import Enemies, Missiles, Player
from threading import Thread
import winsound



# Global Variables
ENEMIES = []
MISSILES = []
ENEMY_MISSILES = []
BUNKERS = []
###################



def main():
    overall = True
    f.setCanvas()
    music_thread = Thread(target=f.music,daemon=True)
    music_thread.start()


    while overall:


        # Initialise variables and lists
        menu = True
        gamePlay = True
        multiplayer = False
        levelCount = 1
        f.SCORE = 0

        playerGraphic = Picture("player1.PNG")
        player_last_fired = 0
        player2_last_fired = 0

        f.populateENEMIES(ENEMIES)
        ################################


        # Draw menu and check player input
        while menu:
            s.clear()
            s.picture(Picture("MainMenu.PNG"))
            s.show(1)

            key = s.getKeysPressed()

            if key[s.K_p]:
                menu = False
                highscore = f.update_highscore('highscore_file.txt', 0)
            if key[s.K_q]:
                overall = False
                menu = False
                gamePlay = False
            if key[s.K_i]:
                f.drawControls()
            if key[s.K_c]:
                playerGraphic = f.playerChoice()
            if key[s.K_m]:
                highscore = f.update_highscore('highscore_file.txt', 0)
                multiplayer = True
                menu = False
        ###################################


        # Initialise player object/s
        player = Player(0,25, math.pi/2, playerGraphic,1)

        if multiplayer:
            player2 = Player(125,25,math.pi/2,playerGraphic,1)
            player._x = -125
        ###################################


        # Display level 1
        if gamePlay:
            levelCount = f.levelDisplay(levelCount)
        ###################################


        # Actual game
        while gamePlay:
            # Initialise background and user input
            key = s.getKeysPressed()
            s.clear()
            s.picture(Picture("background.PNG"))
            f.score()
            f.highscore(highscore)
            ######################################


            # Check player input
            if key[s.K_a]:
                player.move('left')
            if key[s.K_d]:
                player.move('right')
            if key[s.K_4]:
                player.moveCannon('left')
            if key[s.K_6]:
                player.moveCannon('right')
            if key[s.K_SPACE] and (time.time() - player_last_fired > .9) and player._hitpoints > 0:
                MISSILES.append(Missiles(player._x, player._y, player._theta, 0))
                pew_thread = Thread(target=winsound.PlaySound, args=("pew.wav", winsound.SND_FILENAME))
                pew_thread.start() 
                player_last_fired = time.time()
            if key[s.K_q]:
                overall = False
                gamePlay = False
            if key[s.K_e]:
                gamePlay = False
            #####################################


            # Counterattack, move everything and draw next frame, check hits and game status
            if levelCount > 2:
                f.enemyCounterattack(player._x, ENEMY_MISSILES, ENEMIES)

            f.moveEverything(ENEMIES, MISSILES, ENEMY_MISSILES, player, BUNKERS)  

            f.checkForHits(ENEMIES, BUNKERS, MISSILES, ENEMY_MISSILES)
            f.checkIfPlayerHit(player, ENEMY_MISSILES, ENEMIES)

            gameStatus = f.gameStatus(ENEMIES, ENEMY_MISSILES, player)
            #######################################################################


            # Ends game if the player is dead
            # Loads next level if current level has been cleared
            if (player._hitpoints <= 0 and multiplayer == False):
                gamePlay = False
            if gameStatus == 'WON' and multiplayer == False:
                levelCount = f.levelDisplay(levelCount)
                ENEMIES.clear()
                MISSILES.clear()
                ENEMY_MISSILES.clear()
                BUNKERS.clear()

                if levelCount > 4:
                    f.ENEMY_HITPOINTS += 1
                if levelCount > 4:
                    f.ENEMY_SPEED += 0.5
                f.populateENEMIES(ENEMIES)
                
                if levelCount > 3:
                    f.populateBUNKERS(BUNKERS)
            #######################################################################
        

            # Multiplayer mode
            if multiplayer:
                # Draws player 2
                player2.draw()
                player2.drawCannon()
                ##########################################


                # Checks player 2 input
                if key[s.K_j]:
                    player2.move('left')
                if key[s.K_l]:
                    player2.move('right')
                if key[s.K_LEFT]:
                    player2.moveCannon('left')
                if key[s.K_RIGHT]:
                    player2.moveCannon('right')
                if key[s.K_RCTRL] and (time.time() - player2_last_fired > .9) and player2._hitpoints > 0:
                    MISSILES.append(Missiles(player2._x, player2._y, player2._theta, 0))
                    pew2_thread = Thread(target=winsound.PlaySound, args=("pew.wav", winsound.SND_FILENAME))
                    pew2_thread.start() 
                    player2_last_fired = time.time()
                ############################################


                # Counterattacks and checks for hits on player two
                if levelCount > 2:
                    f.enemyCounterattack(player2._x, ENEMY_MISSILES, ENEMIES)

                if player2._hitpoints > 0:
                    f.checkIfPlayerHit(player2, ENEMY_MISSILES, ENEMIES)
                ###############################################


                # Ends game if both players are dead or level 4 has been reached
                # Loads next level and respawns both players if current level has been cleared 
                if (player._hitpoints <= 0 and player2._hitpoints <= 0) or (gameStatus == 'WON' and levelCount == 4):
                    gamePlay = False
                if gameStatus == 'WON' and levelCount < 4:
                    levelCount = f.levelDisplay(levelCount)
                    ENEMIES.clear()
                    MISSILES.clear()
                    ENEMY_MISSILES.clear()
                    f.populateENEMIES(ENEMIES)
                    player = Player(-125,25, math.pi/2, playerGraphic,1)
                    player2 = Player(125,25,math.pi/2,playerGraphic,1)
                ###################################################################
            ###########################################################################################
            
            s.show(0)

        # Clears unit lists and displays game over screen when the game is over
        ENEMIES.clear()
        MISSILES.clear()
        ENEMY_MISSILES.clear()
        BUNKERS.clear()
        if overall and not key[s.K_e]:
            prevhighscore = f.update_highscore('highscore_file.txt', highscore)
            f.gameOver(levelCount, highscore, prevhighscore)
        ################################################################





if __name__ == '__main__': main()
