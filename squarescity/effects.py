import random

from cocos.sprite import Sprite
from cocos.actions import CallFunc, Delay

import pyglet.image


class Explosion(Sprite):

    def __init__(self, x, y):
        img_seq = pyglet.image.load('data/boom.png')
        grid = pyglet.image.ImageGrid(img_seq, 1, 9)
        anim = grid.get_animation(0.02 + random.uniform(-0.015, 0.015), False)
        super(Explosion, self).__init__(anim)
        self.x, self.y = x + random.uniform(-4, 4), y + random.uniform(-4, 4)
        self.rotation = random.uniform(-3.14, 3.14)

        self.do(Delay(anim.get_duration()) + CallFunc(self.kill))
