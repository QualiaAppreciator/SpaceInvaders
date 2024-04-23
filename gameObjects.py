import math
import stddraw as s
import functions as f
from picture import Picture

RADIUS = 20 #
ANGULAR_SPEED = .025 

class Enemies:
    def __init__(self, x, y, speed, hitpoints): 
        self._x = x
        self._y = y
        self._speed = speed 
        self._hitpoints = hitpoints
        self._graphic = Picture("enemy.PNG")

    def move(self):
        if abs(self._x + self._speed) + self._graphic.width()/2 > 250:
            self._speed = -self._speed
            self._y -= 14
        self._x += self._speed

    def draw(self):
        s.picture(self._graphic, self._x, self._y)

class Missiles:
    def __init__(self, x, y, theta):
        self._x = x
        self._y = y
        self._theta = theta
        self._speed = 5

    def move(self):
        if self._theta <= math.pi/2:
            self._x -= self._speed*math.cos(self._theta)
            self._y += self._speed*math.sin(self._theta)
        else:
            self._x += self._speed*math.sin(self._theta-math.pi/2)
            self._y += self._speed*math.cos(self._theta-math.pi/2)

    def draw(self):
        s.setPenColor(s.WHITE)
        s.filledCircle(self._x, self._y, 3)

class Player:
    def __init__(self, x, y, theta, graphic):
        self._x = x
        self._y = y
        self._theta = theta 
        self._graphic = graphic
        self._speed = 1

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
        s.picture(self._graphic, self._x, self._y)

    def moveCanon(self, key):
        if key == 'j':
            self._theta -= ANGULAR_SPEED
            if self._theta <= 0:
                self._theta = 0
        if key == 'l':
            self._theta += ANGULAR_SPEED
            if self._theta >= math.pi:
                self._theta = math.pi

    def drawCanon(self):
        s.setPenColor(s.BLACK)
        s.setPenRadius(2.5)
        if self._theta <= math.pi/2:
            s.line(self._x, self._y, self._x-RADIUS*math.cos(self._theta), self._y+RADIUS*math.sin(self._theta))
        else:
            s.line(self._x, self._y, self._x+RADIUS*math.sin(self._theta-math.pi/2), self._y+RADIUS*math.cos(self._theta-math.pi/2))

def main():
    pass

if __name__ == '__main__': main()