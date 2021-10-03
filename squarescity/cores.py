from cocos.sprite import Sprite
from cocos.euclid import Vector2


class Core(Sprite):

    def __init__(self, position):
        super(Core, self).__init__("data/core.png")
        self.x, self.y = position

    def intersects(self, rect):
        core_center = Vector2(self.x, self.y)
        rect_center = Vector2(*rect.center)

        distance_squared = (core_center - rect_center).magnitude_squared()

        return distance_squared < (self.width / 2.0 + rect.width / 2.0) ** 2
