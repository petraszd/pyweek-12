from cocos.sprite import Sprite


class Wall(Sprite):

    def __init__(self, position):
        super(Wall, self).__init__("data/wall.png")
        self.x, self.y = position
