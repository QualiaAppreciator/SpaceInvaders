import stddraw as s
import math, time
from gameObjects import Enemies, Missiles, Bunker
from picture import Picture
import stdaudio



# Global variables
ENEMY_LAST_FIRED = 0
SCORE = 0
ENEMY_SPEED = 1.5
ENEMY_HITPOINTS = 1
######################



# Added by Josh
# Initialises the canvas
def setCanvas():
    s.setCanvasSize(950,600)
    s.setXscale(-250,250)
    s.setYscale(0,500)
    s.setFontSize(16)




# Added by Mikael
# Plays background music
def music():
    for i in range(0, 10):
        stdaudio.playFile("Backtrack")




# Added by Josh
# Initialises Enemy objects and places them in list ENEMIES
def populateENEMIES(ENEMIES):
    y = 450
    for i in range(3):
        x = -100
        for j in range(7):
            ENEMIES.append(Enemies(x,y,ENEMY_HITPOINTS,ENEMY_SPEED))
            x += 50
        y -= 50




# Written by Mikael
# Initialises Bunker objects and places them in list BUNKERS
def populateBUNKERS(BUNKERS):
    BUNKERS.append(Bunker(-140,170,4))
    BUNKERS.append(Bunker(0,170,6))
    BUNKERS.append(Bunker(140,170,4))




# Added by Josh
# Displays the game controls, returns to main menu if [b] is pressed
def drawControls():
    display_controls = True

    while display_controls:
        s.clear()
        quit = s.getKeysPressed()
        if quit[s.K_b]:
            display_controls = False
        s.picture(Picture("Controls.PNG"))
        s.show(1)
 



# Added by Josh
# Displays a character choice menu and allows the player to choose a graphic as their character
def playerChoice():
    choice = True
    s.picture(Picture("Characters.PNG"))
    s.picture(Picture("player1.PNG"),-70, 250)
    s.picture(Picture("player2.PNG"),70, 250)

    while choice:
        key = s.getKeysPressed()
        s.show(1)
        if key[s.K_1]:
            return Picture("player1.PNG")
        if key[s.K_2]:
            return Picture("player2.PNG")
        



# Added by Josh
# Displays the level about to be played and returns that level incremented by one 
def levelDisplay(levelCount):
    currentTime = time.time()
    s.clear(s.BLACK)
    s.setFontSize(30)
    s.setPenColor(s.WHITE)
    while time.time() - currentTime <= 2:
        s.text(0,250,"LEVEL " + str(levelCount))
        s.show(1)
    return levelCount + 1




# Added by Mikael 
# Displays the current score in the top left corner
def score():
    s.setPenColor(s.PINK)
    s.setFontSize(20)
    s.text(-220,485,"SCORE = " + str(SCORE))




#Written by Nico
#displays previous high score
def highscore(highscore):
    s.setPenColor(s.PINK)
    s.setFontSize(20)
    s.text(190, 485, "HIGHSCORE = " + str(highscore))




# Added by Mikael
# Enemy counterattacks if the four conditions below are met 
def enemyCounterattack(playerx, ENEMY_MISSILES, ENEMIES):
    global ENEMY_LAST_FIRED
    for i in range(0, len(ENEMIES)):

        # Initialise booleans separately for clarity
        player_below_enemy = abs(playerx - ENEMIES[i]._x) < 20
        no_other_enemy_below = (i < 7 and ENEMIES[i+7]._hitpoints == 0 and ENEMIES[i+14]._hitpoints == 0) \
                                    or (i >= 7 and i < 14 and (ENEMIES[i+7]._hitpoints == 0)) \
                                    or (i >= 14)
        enemy_alive = ENEMIES[i]._hitpoints != 0
        recharge_time_elapsed = time.time() - ENEMY_LAST_FIRED > 1.9
        ############################################################


        if player_below_enemy and enemy_alive and no_other_enemy_below and recharge_time_elapsed:
            ENEMY_MISSILES.append(Missiles(ENEMIES[i]._x, ENEMIES[i]._y, 0, 1))

            ENEMY_LAST_FIRED = time.time()




# Added by Josh and Mikael
# Moves and redraws everything by one frame
def moveEverything(ENEMIES, MISSILES, ENEMY_MISSILES, player, BUNKERS):
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




# Written by Mikael and Josh
# Checks if any of the Missiles fired by the player is touching an enemy,
# if it is, lowers that enemy's hitpoints by 1 and removes the Missile object from MISSILES
# Increases enemy speed if an enemy is hit
# Removes a Missile object from MISSILES if it moves out of the borders of the game
def checkForHits(ENEMIES, BUNKERS, MISSILES, ENEMY_MISSILES):
    global SCORE

    for i in ENEMIES:
        for j in MISSILES:
            if (math.sqrt((i._x-j._x)**2+(i._y-j._y)**2) <= 18) and i._hitpoints != 0:
                i._hitpoints -= 1
                
                for u in ENEMIES:
                    if u._speed > 0:
                        u._speed += 0.05
                    else:
                        u._speed -= 0.05

                MISSILES.remove(j)
                SCORE += 10
        

    for i in BUNKERS:
        for j in MISSILES:
            if (math.sqrt((i._x-j._x)**2+(i._y-j._y)**2) <= 35) and i._hitpoints != 0:
                i._hitpoints -= 1
                MISSILES.remove(j)
                if i._hitpoints == 0:
                    SCORE += 5

        for k in ENEMY_MISSILES:
            if (math.sqrt((i._x-k._x)**2+(i._y-k._y)**2) <= 35) and i._hitpoints != 0:
                i._hitpoints -= 1
                ENEMY_MISSILES.remove(k)
        
    
    for i in MISSILES:
        if i._x < -250 or i._x > 250 or i._y > 500:
            MISSILES.remove(i)




# Added by Josh and Mikael
# Checks if the player has been hit
def checkIfPlayerHit(player, ENEMY_MISSILES, ENEMIES):
    for i in ENEMY_MISSILES:
        if math.sqrt((player._x-i._x)**2+(player._y-i._y)**2) <= 30:
            player._hitpoints -= 1
            ENEMY_MISSILES.remove(i)
    for j in ENEMIES:
        if (math.sqrt((player._x-j._x)**2 + (player._y-j._y)**2) <= 30) and j._hitpoints != 0:
            player._hitpoints = 0





# Written by Mikael and Josh
# Checks status of the game
# Returns 'LOST' if an enemy missile or an enemy touches the player,
# or an enemy touches the bottom border
# Returns 'WON' if all enemies are dead
def gameStatus(ENEMIES, ENEMY_MISSILES, player):
    living_enemies = 0
    for g in ENEMIES:
        if g._hitpoints != 0:
            living_enemies += 1
    if living_enemies == 0:
        return 'WON'



# Added by Nico
# Updates highscore
def update_highscore(highscore_file, highscore):
    file = open(highscore_file, 'r')
    current_highscore = int(file.read())
    file.close()
    if SCORE >= current_highscore:
        file = open(highscore_file, 'w')
        file.write(str(SCORE))
        file.close()
        highscore = SCORE
    else:
        highscore = current_highscore
    return highscore




# Written by Mikael and Josh
# Displays the GAME OVER message and the most recently played game's statistics
def gameOver(levelCount, highscore, prevhighscore):
    display_gameover = True

    while display_gameover:
        s.clear()

        quit = s.getKeysPressed()
        if quit[s.K_r]:
            display_gameover = False

        s.picture(Picture("GameOver.PNG"))
        s.setFontSize(35)
        s.setPenColor(s.WHITE)
        s.text(30,290,str(SCORE))
        s.text(30,240,str(levelCount-1))
        s.text(30,180,str(highscore))
        s.show(1)
