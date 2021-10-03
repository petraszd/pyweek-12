import pyglet

from cocos.scene import Scene
from cocos.menu import Menu, MenuItem
from cocos.director import director
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.scenes.transitions import FadeBLTransition
from cocos.actions import Delay, CallFunc, MoveTo, MoveBy, Repeat

from squarescity.game import Level1
from squarescity import config as c


class BlackMenuItem(MenuItem):

    def generateWidgets (self, pos_x, pos_y, font_item, font_item_selected):
        super(BlackMenuItem, self).generateWidgets(pos_x, pos_y,
                                                   font_item,
                                                   font_item_selected)
        self.item.color = (0, 0, 0, 255)
        self.item_selected.color = (255, 255, 255, 255)


class GameMenu(Menu):
    def __init__(self):
        super(GameMenu, self).__init__()

        items = [BlackMenuItem('Start a Game', self.start_game),
                 BlackMenuItem('How to play', self.help_screen),
                 BlackMenuItem('Credits', self.credits),
                 BlackMenuItem('Quit', self.quit)]
        self.create_menu(items)

    def start_game(self):
        director.replace(FadeBLTransition(Scene(Level1(NextLevelScene,
                                                       GameOverScene,
                                                       WinScene))))

    def help_screen(self):
        director.replace(FadeBLTransition(AboutScene()))

    def credits(self):
        director.replace(FadeBLTransition(CreditsScene()))

    def quit(self):
        director.pop()

    def on_quit(self):
        self.quit()


class ImageScene(Scene):

    def __init__(self):
        super(ImageScene, self).__init__()
        back = Sprite(self.get_image_filename())
        back.x = c.WIDTH / 2
        back.y = c.HEIGHT / 2
        self.add(back, z=0)

    def get_image_filename(self):
        raise NotImplementedError


class StartScene(ImageScene):

    def __init__(self):
        super(StartScene, self).__init__()
        self.add(GameMenu(), z=1)

    def get_image_filename(self):
        return 'data/start-screen.png'


class PreviewLayer(Layer):

    is_event_handler = True

    def on_key_press(self, symbol, modifiers):
        if symbol != pyglet.window.key.ESCAPE:
            director.replace(FadeBLTransition(StartScene()))

    def on_mouse_press(self, x, y, button, modifiers):
        director.replace(FadeBLTransition(StartScene()))


class PreviewScene(ImageScene):

    def __init__(self):
        super(PreviewScene, self).__init__()
        self.add(PreviewLayer())


class AboutScene(PreviewScene):

    def get_image_filename(self):
        return 'data/about-screen.png'


class CreditsScene(PreviewScene):

    def get_image_filename(self):
        return 'data/credits-screen.png'


class WinScene(Scene):

    def __init__(self):
        super(WinScene, self).__init__()
        sprite = Sprite('data/win-screen.png')
        sprite.x = sprite.width / 2
        sprite.y = sprite.height / 2
        self.add(sprite, z=0)

        self.do(Delay(1.5) + CallFunc(self.winning_animation))

    def winning_animation(self):
        poses = [(210, 340), (240, 280), (270, 220), (270, 160), (270, 100),
                 (300, 280), (330, 340),

                 (460, 340),
                 (430, 280), (410, 220), (390, 160), (370, 100),
                 (490, 280), (510, 220), (530, 160), (550, 100),
                 (460, 160),

                 (590, 340), (620, 280), (650, 220), (650, 160), (650, 100),
                 (680, 280), (710, 340),

                 (810, 340), (810, 280), (810, 220), (810, 100)]

        for i, pos in enumerate(poses):
            self.dance(pos[0] - 40, pos[1], i / 10.0)


    def dance(self, x, y, delay):
        square = Sprite('data/dancing-one.png')
        square.x = -60
        square.y = y
        self.add(square, z=1)

        loop = Repeat(MoveBy((-5.0, 0.0), 0.1) + MoveBy((5.0, 0.0), 0.1))
        square.do(Delay(delay) + MoveTo((x, y), 0.5) + loop)


class GameOverScene(Scene):

    def __init__(self, level_class):
        super(GameOverScene, self).__init__()
        self.level_class = level_class

        sprite = Sprite(self.get_image_filename())
        sprite.x = sprite.width / 2
        sprite.y = sprite.height / 2
        self.add(sprite)

        self.do(Delay(2.0) + CallFunc(self.start_level))

    def start_level(self):
        level = self.level_class(NextLevelScene,
                                 GameOverScene,
                                 WinScene)
        director.replace(FadeBLTransition(Scene(level)))

    def get_image_filename(self):
        return 'data/lose-screen.png'


class NextLevelScene(Scene):

    def __init__(self, level_class):
        super(NextLevelScene, self).__init__()
        self.level_class = level_class
        sprite = Sprite('data/next-screen.png')
        sprite.x = sprite.width / 2
        sprite.y = sprite.height / 2
        self.add(sprite)

        self.do(Delay(2.0) + CallFunc(self.start_next_level))


    def start_next_level(self):
        level = self.level_class(NextLevelScene,
                                 GameOverScene,
                                 WinScene)
        director.replace(FadeBLTransition(Scene(level)))
