import stddraw as s
import math, time
from gameObjects import Enemies
from project_main import ENEMY_SPEED, BACKGROUND
from picture import Picture


def setCanvas():
    s.setCanvasSize(500,500)
    s.setXscale(-250,250)
    s.setYscale(0,500)
    s.setFontSize(16)



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



def populateENEMIES(ENEMIES):
    y = 450
    for i in range(3):
        x = -100
        for j in range(5):
            ENEMIES.append(Enemies(x,y,ENEMY_SPEED,1))
            x += 50
        y -= 50



def checkForHits(ENEMIES, MISSILES, highscore):
    for i in ENEMIES:
        for j in MISSILES:
            if math.sqrt((i._x-j._x)**2+(i._y-j._y)**2) - 18 <= 0:
                ENEMIES.remove(i)
                MISSILES.remove(j)
                highscore += 30
    for i in MISSILES:
        if i._x < -250 or i._x > 250 or i._y > 500:
            MISSILES.remove(i)

    return highscore



def gameStatus(ENEMIES, player):
    if len(ENEMIES) == 0:
        return 'YOU WIN'
    for i in ENEMIES:
        if math.sqrt((player._x-i._x)**2 + (player._y-i._y)**2) <= 50:
            return 'YOU LOSE'



def gameOver(status):
    s.picture(BACKGROUND)
    s.setFontSize(16)
    s.text(0,250,"GAME OVER")
    s.text(0,235,status)
    s.show(1)
    time.sleep(3)



def score(score):
    s.setPenColor(s.WHITE)
    s.setFontSize(16)
    s.text(-210,490,"score = " + str(score))



def levelDisplay(levelCount):
    currentTime = time.time()
    s.clear(s.BLACK)
    s.setFontSize(16)
    s.setPenColor(s.WHITE)
    while time.time() - currentTime <= 2:
        s.text(0,250,"LEVEL " + str(levelCount))
        s.show(1)
    return levelCount + 1



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
