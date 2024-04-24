import stddraw as s
import math, time
from gameObjects import Enemies, Missiles, Player, Bunker
from project_main import BACKGROUND
from picture import Picture

ENEMY_LAST_FIRED = 0

# Added by Josh
# Initialises the canvas
def setCanvas():
    s.setCanvasSize(500,500)
    s.setXscale(-250,250)
    s.setYscale(0,500)
    s.setFontSize(16)


# Added by Josh
# Displays the main menu
def drawMenu():
    s.clear()
    s.setPenColor(s.WHITE)
    s.setFontSize(16)
    s.picture(BACKGROUND)
    s.text(0,250,"Press p to play")
    s.text(0,238,"Press i for instructions")
    s.text(0,226,"Press c to choose character")
    s.text(0,214,"Press e to come back")
    s.text(0,202,"Press q to quit")
    s.show(1)


# Added by Josh
# Displays the game instructions
def drawInstructions():
    instructions = True 
    while instructions:
        s.clear()
        Quit = s.getKeysPressed()
        if Quit[s.K_b]:
            instructions = False
        s.picture(BACKGROUND)
        s.text(0,275,"To move left press: ' a '")
        s.text(0,260,"To move right press: ' d '")
        s.text(0,245,"To shift the cannon angle left press: ' j '")
        s.text(0,230,"To shift the cannon angle right press: ' l '")
        s.text(0,215,"To shoot press: SPACE BAR")
        s.text(0,200,"Press ' b ' to return to the main menu")
        s.show(1)


# Added by Josh
# Puts Enemy objects and their initial conditions in the list ENEMIES
def populateENEMIES(ENEMIES):
    y = 450
    for i in range(3):
        x = -100
        for j in range(5):
            ENEMIES.append(Enemies(x,y,1))
            x += 50
        y -= 50


# Written by Mikael
def populateBUNKERS(BUNKERS):
    BUNKERS.append(Bunker(-140,170,4))
    BUNKERS.append(Bunker(0,170,6))
    BUNKERS.append(Bunker(140,170,4))


# Written by Mikael and Josh
# Checks if any of the Missiles fired by the player is touching an enemy,
# if it is, lowers that enemy's hitpoints by 1 and removes the Missile object from MISSILES
# Removes a Missile object from MISSILES if it moves out of the borders of the game
def checkForHits(ENEMIES, BUNKERS, MISSILES, highscore):
    for i in ENEMIES:
        for j in MISSILES:
            if (math.sqrt((i._x-j._x)**2+(i._y-j._y)**2) <= 18) and i._hitpoints != 0:
                i._hitpoints -= 1
                MISSILES.remove(j)
                highscore += 30

    for i in BUNKERS:
        for j in MISSILES:
            if (math.sqrt((i._x-j._x)**2+(i._y-j._y)**2) <= 40) and i._hitpoints != 0:
                i._hitpoints -= 1
                MISSILES.remove(j)
                if i._hitpoints == 0:
                    highscore += 20
    
    for i in MISSILES:
        if i._x < -250 or i._x > 250 or i._y > 500:
            MISSILES.remove(i)

    return highscore


# Written by Mikael
# Enemy fires Missile if the enemy is above the player,
# it is alive,
# there isn't an enemy below it,
# and the recharge time has elapsed
def enemyCounterattack(player, ENEMY_MISSILES, ENEMIES):
    global ENEMY_LAST_FIRED
    for i in range(0, len(ENEMIES)):
        if (abs(player._x - ENEMIES[i]._x) < 25) \
            and ENEMIES[i]._hitpoints != 0 \
            and ((i < 5 and ENEMIES[i+5]._hitpoints == 0 and ENEMIES[i+10]._hitpoints == 0) \
                or (i >= 5 and i < 10 and (ENEMIES[i+5]._hitpoints == 0)) \
                or (i >= 10)) \
            and (time.time() - ENEMY_LAST_FIRED > 1.5) and player._hitpoints > 0:

            ENEMY_MISSILES.append(Missiles(ENEMIES[i]._x, ENEMIES[i]._y, 0, 1))
            ENEMY_LAST_FIRED = time.time()

# Written by Mikael and Josh
# Checks status of the game
# Returns 'LOST' if an enemy missile or an enemy touches the player,
# or an enemy touches the bottom border
# Returns 'WON' if all enemies are dead
def gameStatus(ENEMIES, ENEMY_MISSILES):
    living_enemies = 0
    for g in ENEMIES:
        if g._hitpoints != 0:
            living_enemies += 1
    if living_enemies == 0:
        return 'WON'

# Written by Mikael and Josh
# Displays the GAME OVER message and the most recently played game's statistics
def gameOver(levelCount, score):
    s.picture(BACKGROUND)
    s.setFontSize(16)
    s.text(0,250,"GAME OVER")
    s.text(0,235,"Final score: " + str(score))
    s.text(0,220,"Level reached: " + str(levelCount-1))
    s.show(1)
    time.sleep(3)


# Added by Mikael 
# Displays the current score in the top left corner
def score(score):
    s.setPenColor(s.WHITE)
    s.setFontSize(16)
    s.text(-210,490,"score = " + str(score))


# Added by Josh
# Displays the level about to be played and returns that level incremented by one 
def levelDisplay(levelCount):
    currentTime = time.time()
    s.clear(s.BLACK)
    s.setFontSize(16)
    s.setPenColor(s.WHITE)
    while time.time() - currentTime <= 2:
        s.text(0,250,"LEVEL " + str(levelCount))
        s.show(1)
    return levelCount + 1


# Written by Josh
# Displays a character choice menu and allows the player to choose a graphic as their character
# This function is accessed from the game menu
def playerChoice():
    choice = True
    s.picture(BACKGROUND)
    s.setFontSize(26)
    s.text(0,320,"Choose your character")
    s.picture(Picture('player1.PNG'),-50, 250)
    s.picture(Picture('player2.PNG'),50, 250)
    s.setFontSize(20)
    s.text(-50, 200, "1")
    s.text(50, 200, "2")

    while choice:
        key = s.getKeysPressed()
        s.show(1)
        if key[s.K_1]:
            return Picture('player1.PNG')
        if key[s.K_2]:
            return Picture('player2.PNG')

def checkIfPlayerHit(player, ENEMY_MISSILES, ENEMIES):
    for i in ENEMY_MISSILES:
        if math.sqrt((player._x-i._x)**2+(player._y-i._y)**2) <= 35:
            player._hitpoints -= 1
            ENEMY_MISSILES.remove(i)
    for j in ENEMIES:
        if math.sqrt((player._x-j._x)**2 + (player._y-j._y)**2) <= 50:
            player._hitpoints = 0
    return player._hitpoints
