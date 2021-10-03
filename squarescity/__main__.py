from cocos.director import director

from squarescity.scenes import StartScene
from squarescity import config as c
from squarescity.music import play_background_music


def main():
    director.init(width=c.WIDTH, height=c.HEIGHT)
    play_background_music()
    return director.run(StartScene())
