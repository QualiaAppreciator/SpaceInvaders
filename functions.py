import stddraw as s
import math, time
from gameObjects import Enemies, Missiles, Bunker
from project_main import BACKGROUND
from picture import Picture
import stdaudio
from threading import Thread
import winsound

ENEMY_LAST_FIRED = 0
SCORE = 0

# Added by Mikael
def music():
    for i in range(0, 10):
        stdaudio.playFile("Backtrack")



# Added by Josh
# Initialises the canvas
def setCanvas():
    s.setCanvasSize(950,600)
    s.setXscale(-250,250)
    s.setYscale(0,500)
    s.setFontSize(16)


# Added by Josh
# Displays the main menu
def drawMenu():
    s.clear()
    s.picture(Picture("MainMenu.PNG"))
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
        s.picture(Picture("Instructions.PNG"))
        s.show(1)


# Written by Josh
# Displays a character choice menu and allows the player to choose a graphic as their character
# This function is accessed from the game menu
def playerChoice():
    choice = True
    s.picture(Picture("Characters.PNG"))
    s.picture(Picture('player1.PNG'),-70, 250)
    s.picture(Picture('player2.PNG'),70, 250)

    while choice:
        key = s.getKeysPressed()
        s.show(1)
        if key[s.K_1]:
            return Picture('player1.PNG')
        if key[s.K_2]:
            return Picture('player2.PNG')
        

# Added by Josh
# Puts Enemy objects and their initial conditions in the list ENEMIES
def populateENEMIES(ENEMIES):
    y = 450
    for i in range(3):
        x = -100
        for j in range(7):
            ENEMIES.append(Enemies(x,y,1))
            x += 50
        y -= 50


# Written by Mikael
def populateBUNKERS(BUNKERS):
    BUNKERS.append(Bunker(-140,170,4))
    BUNKERS.append(Bunker(0,170,6))
    BUNKERS.append(Bunker(140,170,4))



# Moved by Mikael
# Moved from main for modularity
def moveEverything(ENEMIES, MISSILES, ENEMY_MISSILES, BUNKERS, player):
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
# Removes a Missile object from MISSILES if it moves out of the borders of the game
def checkForHits(ENEMIES, BUNKERS, MISSILES, ENEMY_MISSILES):
    global SCORE

    for i in ENEMIES:
        for j in MISSILES:
            if (math.sqrt((i._x-j._x)**2+(i._y-j._y)**2) <= 23) and i._hitpoints != 0:
                i._hitpoints -= 1
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


# Written by Mikael
# Enemy fires Missile if the enemy is above the player,
# it is alive,
# there isn't an enemy below it,
# and the recharge time has elapsed
def enemyCounterattack(playerx, ENEMY_MISSILES, ENEMIES):
    global ENEMY_LAST_FIRED

    for i in range(0, len(ENEMIES)):
        player_below_enemy = abs(playerx - ENEMIES[i]._x) < 22
        no_other_enemy_below = (i < 7 and ENEMIES[i+7]._hitpoints == 0 and ENEMIES[i+14]._hitpoints == 0) \
                                    or (i >= 7 and i < 14 and (ENEMIES[i+7]._hitpoints == 0)) \
                                    or (i >= 14)
        enemy_alive = ENEMIES[i]._hitpoints != 0
        recharge_time_elapsed = time.time() - ENEMY_LAST_FIRED > 1.5

        if player_below_enemy and enemy_alive and no_other_enemy_below and recharge_time_elapsed:
            ENEMY_MISSILES.append(Missiles(ENEMIES[i]._x, ENEMIES[i]._y, 0, 1))
            ENEMY_LAST_FIRED = time.time()
            enemy_pew_thread = Thread(target=winsound.PlaySound, args=("enemy_pew.wav", winsound.SND_FILENAME))
            enemy_pew_thread.start()



# Written by Mikael and Josh
# Checks status of the game
# Returns 'LOST' if an enemy missile or an enemy touches the player,
# or an enemy touches the bottom border
# Returns 'WON' if all enemies are dead
def gameStatus(ENEMIES, player, ENEMY_MISSILES):
    living_enemies = 0
    for g in ENEMIES:
        if g._hitpoints != 0:
            living_enemies += 1
    if living_enemies == 0:
        return 'WON'
    
    for i in ENEMIES:
        if math.sqrt((player._x-i._x)**2 + (player._y-i._y)**2) <= 40:
            return 'LOST'
        
    for j in ENEMY_MISSILES:
        if math.sqrt((player._x-j._x)**2+(player._y-j._y)**2) <= 20:
            return 'LOST'


# Written by Mikael and Josh
# Displays the GAME OVER message and the most recently played game's statistics
def gameOver(levelCount):
    s.picture(Picture("GameOver.PNG"))
    s.setFontSize(35)
    s.setPenColor(s.WHITE)
    s.text(30,290,str(SCORE))
    s.text(30,240,str(levelCount-1))
    s.show(1)
    time.sleep(3)


# Added by Mikael 
# Displays the current score in the top left corner
def score():
    s.setPenColor(s.PINK)
    s.setPenRadius(1.5)
    s.setFontSize(20)
    s.text(-220,485,"SCORE = " + str(SCORE))


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
