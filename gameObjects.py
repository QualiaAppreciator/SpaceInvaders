import math
import stddraw as s
import functions as f
from picture import Picture




class Enemies:
    def __init__(self, x, y, hitpoints, speed): 
        self._x = x
        self._y = y
        self._speed = speed
        self._hitpoints = hitpoints
        self._graphic = Picture("enemy.PNG")

    def move(self):
        if abs(self._x + self._speed) + self._graphic.width()/2 > 250:
            self._speed = -self._speed
            self._y -= 35
        self._x += self._speed

    def draw(self):
        if self._hitpoints != 0:
            s.picture(self._graphic, self._x, self._y)




# Contains both player and enemy missiles
class Missiles:
    def __init__(self, x, y, theta, enemy):
        self._x = x
        self._y = y
        self._theta = theta
        self._speed = 2.5
        self._enemy = enemy

        if self._enemy == 0:
            if self._theta >= 2*math.pi/5 and self._theta <= 3*math.pi/5:
                self._graphic = Picture("missile1.PNG")
            elif self._theta >= math.pi/5 and self._theta <= 2*math.pi/5:
                self._graphic = Picture("missile1_slant_right.PNG")
            elif self._theta >= 3*math.pi/5 and self._theta <= 4*math.pi/5:
                self._graphic = Picture("missile1_slant_left.PNG")
            elif self._theta <= math.pi/5 and self._theta >= 0:
                self._graphic = Picture("missile1_right.PNG")
            else:
                self._graphic = Picture("missile1_left.PNG")
        else:
            self._graphic = Picture("missile2.PNG")

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



# Added by Josh
class Player:
    def __init__(self, x, y, theta, graphic, hitpoints):
        self._x = x
        self._y = y
        self._theta = theta 
        self._graphic = graphic
        self._speed = 1
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
            self._theta -= 0.03
            if self._theta <= 0:
                self._theta = 0
        if key == 'l':
            self._theta += 0.03
            if self._theta >= math.pi:
                self._theta = math.pi



    def drawCannon(self):
        cannon_radius = 20
        
        if self._hitpoints > 0:
            s.setPenColor(s.GRAY)
            s.setPenRadius(2)

            if self._theta <= math.pi/2:
                s.line(self._x, self._y, self._x-cannon_radius*math.cos(self._theta), self._y+cannon_radius*math.sin(self._theta))
            else:
                s.line(self._x, self._y, self._x+cannon_radius*math.sin(self._theta-math.pi/2), self._y+cannon_radius*math.cos(self._theta-math.pi/2))


# Added by Mikael
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
