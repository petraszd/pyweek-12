import random

from cocos.sprite import Sprite
from cocos.actions import Repeat, MoveBy, CallFunc
from cocos.euclid import Vector2

from squarescity import config as c


class Square(Sprite):

    def __init__(self, position, direction=None):
        super(Square, self).__init__(self.get_imagename())
        self.x, self.y = position

        self.direction = self.calculate_direction(direction)

        move_action = MoveBy(self.direction * c.SQUARE_SPEED, c.SQUARE_TIME)
        func_action = CallFunc(self.is_in_outzone)
        self.do(Repeat(func_action + move_action))

    def shoot(self, direction, distance):
        self.stop()
        move_action = MoveBy(direction * distance * c.SQUARE_SHOOT_SPEED,
                             c.SQUARE_TIME)
        self.do(Repeat(move_action))

    def get_imagename(self):
        return ''

    def is_in_outzone(self):
        if self.x <= c.OUT_ZONE:
            return

        self.stop()
        move_action = MoveBy(self.direction * c.SQUARE_OUT_SPEED,
                             c.SQUARE_TIME)
        self.do(Repeat(move_action))

    def split(self):
        self.kill()
        new_squares = []
        for y in xrange(-1, 2):
            for x in xrange(-1, 2):
                sx = self.x + x * (self.width / 3)
                sy = self.y + y * (self.height / 3)
                smaller = self.get_smallersquare((sx, sy),
                                                 Vector2(x, y).normalized())
                new_squares.append(smaller)
        return new_squares

    def get_smallersquare(self, position, direction):
        return Square(position, direction)

    def calculate_direction(self, start_direction=None):
        direction = Vector2((random.random() - 0.5) / c.SQUARE_X_REDUCER,
                    (random.random() - 0.5) / c.SQUARE_Y_REDUCER)
        direction.normalize()
        if start_direction:
            direction = direction * 0.2 + start_direction * 0.8
        return direction

    def can_cause_big_impact(self):
        return False


class BigSquare(Square):

    def get_imagename(self):
        return "data/3x.png"

    def get_smallersquare(self, position, direction):
        return MiddleSquare(position, direction)

    def can_cause_big_impact(self):
        return True


class MiddleSquare(Square):

    def get_imagename(self):
        return "data/2x.png"

    def get_smallersquare(self, position, direction):
        return SmallSquare(position, direction)


class SmallSquare(Square):

    def get_imagename(self):
        return "data/1x.png"

    def split(self):
        return []
