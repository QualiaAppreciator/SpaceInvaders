import math
import stddraw as s
import functions as f
from picture import Picture

RADIUS = 20
ANGULAR_SPEED = .02

class Enemies:
    def __init__(self, x, y, hitpoints): 
        self._x = x
        self._y = y
        self._speed = 1 
        self._hitpoints = hitpoints
        self._graphic = Picture("enemy.PNG")

    def move(self):
        if abs(self._x + self._speed) + self._graphic.width()/2 > 250:
            self._speed = -self._speed
            self._y -= 16
        self._x += self._speed

    def draw(self):
        if self._hitpoints != 0:
            s.picture(self._graphic, self._x, self._y)

class Missiles:
    def __init__(self, x, y, theta, enemy):
        self._x = x
        self._y = y
        self._theta = theta
        self._speed = 2
        self._enemy = enemy

        if self._enemy == 0:
            self._graphic = Picture("missile1.PNG")
        else:
            self._graphic = Picture("missile2_down.PNG")

    def move(self):
        if self._enemy == 0:
            if self._theta <= math.pi/2:
                self._x -= self._speed*math.cos(self._theta)
                self._y += self._speed*math.sin(self._theta)
            else:
                self._x += self._speed*math.sin(self._theta-math.pi/2)
                self._y += self._speed*math.cos(self._theta-math.pi/2)
        else:
            self._y -= 0.7*self._speed

    def draw(self):
        s.picture(self._graphic, self._x, self._y)

class Player:
    def __init__(self, x, y, theta, graphic, hitpoints):
        self._x = x
        self._y = y
        self._theta = theta 
        self._graphic = graphic
        self._speed = 0.8
        self._hitpoints = hitpoints

    def move(self, key):
        if key == 'left':
            if self._x - self._graphic.width()/2 <= -250:
                self._x = self._x
            else:
                self._x -= self._speed
        if key == 'right':
            if self._x + self._graphic.width()/2 >=250:
                self._x = self._x
            else:
                self._x += self._speed

    def draw(self):
        if self._hitpoints > 0:
            s.picture(self._graphic, self._x, self._y)

    def moveCannon(self, key):
        if key == 'j':
            self._theta -= ANGULAR_SPEED
            if self._theta <= 0:
                self._theta = 0
        if key == 'l':
            self._theta += ANGULAR_SPEED
            if self._theta >= math.pi:
                self._theta = math.pi

    def drawCannon(self):
        if self._hitpoints > 0:
            s.setPenColor(s.BLACK)
            s.setPenRadius(2.5)
            if self._theta <= math.pi/2:
                s.line(self._x, self._y, self._x-RADIUS*math.cos(self._theta), self._y+RADIUS*math.sin(self._theta))
            else:
                s.line(self._x, self._y, self._x+RADIUS*math.sin(self._theta-math.pi/2), self._y+RADIUS*math.cos(self._theta-math.pi/2))


# Written by Mikael
class Bunker:
    def __init__(self, x, y, hitpoints):
        self._x = x
        self._y = y
        self._hitpoints = hitpoints

    def draw(self):
        if self._hitpoints != 0:
            if self._hitpoints <= 2:
                s.picture(Picture("bunker5.PNG"), self._x, self._y)
                return
            if self._hitpoints <= 4:
                s.picture(Picture("bunker2.PNG"), self._x, self._y)
                return
            if self._hitpoints <= 6:
                s.picture(Picture("bunker1.PNG"), self._x, self._y)

def main():
    pass

if __name__ == '__main__': main()
