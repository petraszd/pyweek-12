import colorsys
import random

from cocos.layer import ColorLayer
from cocos.draw import Line
from cocos.actions import Repeat, CallFunc, MoveBy, MoveTo, Delay
from cocos.scenes.transitions import FadeBLTransition
from cocos.euclid import Vector2
from cocos.director import director
from cocos.sprite import Sprite

from squarescity.walls import Wall
from squarescity import config as c
from squarescity.effects import Explosion
from squarescity.music import play_shoot, play_explode


class Level(ColorLayer):

    is_event_handler = True

    def __init__(self, next_lvl_class, game_over_class, win_class):
        self.next_lvl_class = next_lvl_class
        self.game_over_class = game_over_class
        self.win_class = win_class

        hue = random.random()
        super(Level, self).__init__(*self.active_zone_background(hue))

        inactive_zone = ColorLayer(*self.inactive_zone_background(hue))
        inactive_zone.x = c.OUT_ZONE
        self.add(inactive_zone, z=0)
        corners = Sprite('data/corners.png')
        corners.x = corners.width / 2
        corners.y = corners.height / 2
        self.add(corners, z=0)
        self.corners = corners

        # Shooting line related stuff
        self.line = Line((0.0, 0.0), (0.0, 0.0), (255, 255, 255, 255))
        self.line.visible = False
        self.add(self.line, z=2)
        self.line_action = None

        self.fill_level()

        self.reset_event_attributes()

        # logic actions
        self.do(Repeat(CallFunc(self.level_event)))

    def fill_level(self):
        self.squares = self.create_squares()
        for square in self.squares:
            self.add(square, z=1)

        self.walls = self.create_walls()
        for wall in self.walls:
            self.add(wall, z=1)

        self.cores = self.create_cores()
        for core in self.cores:
            self.add(core, z=1)

    def active_zone_background(self, hue):
        return self.to_rgb(hue, 0.9, 0.76)

    def inactive_zone_background(self, hue):
        return self.to_rgb(hue, 0.9, 0.66)

    def to_rgb(self, floath, floats, floatv):
        r, g, b = colorsys.hsv_to_rgb(floath, floats, floatv)
        return (int(255 * r), int(255 * g), int(255 * b), 255)

    def create_squares(self):
        return []

    def create_walls(self):
        walls = []
        for position in self.walls_positions():
            walls.append(Wall(position))
        return walls

    def create_cores(self):
        return []

    def walls_positions(self):
        return []

    def split(self, square):
        new_squares = square.split()
        for new_square in new_squares:
            self.add(new_square, z=1)
        self.squares += new_squares

    def reposition_line(self):
        self.line.start = self.mouse_position
        self.line.end = self.selected.x, self.selected.y

    def shoot(self):
        x0, y0 = self.mouse_position
        x1, y1 = self.selected.x, self.selected.y

        v = Vector2(x1 - x0, y1 - y0)

        play_shoot()
        self.selected.shoot(v.normalized(), v.magnitude())

    def level_event(self):
        self.clear_out_of_bounds()
        if not self.check_for_win():
            self.check_for_game_over()
        self.collide()

    def clear_out_of_bounds(self):
        new_squares = []
        for square in self.squares:
            if square.x < -30.0 or square.x > c.WIDTH + 30.0:
                square.kill()
                continue
            if square.y < -30.0 or square.y > c.HEIGHT + 30.0:
                square.kill()
                continue
            new_squares.append(square)
        self.squares = new_squares

    def check_for_win(self):
        if len(self.cores) != 0:
            return False

        self.stop()
        self.do(Delay(1.0) + CallFunc(self.win_actions))
        return True

    def win_actions(self):
        self.corners.visible = False # prevents strange redering artifact
        next_lvl_class = self.get_next_level_class()
        if next_lvl_class:
            director.replace(FadeBLTransition(self.next_lvl_class(next_lvl_class)))
        else:
            director.replace(FadeBLTransition(self.win_class()))

    def check_for_game_over(self):
        if len(self.squares) == 0:
            self.do(Delay(1.0) + CallFunc(self.game_over))

    def game_over(self):
        self.corners.visible = False # prevents strange redering artifact
        self.stop()
        director.replace(FadeBLTransition(self.game_over_class(type(self))))

    def collide(self):
        new_squares = []
        for square in self.squares:
            if square.x < c.OUT_ZONE:
                new_squares.append(square)
                continue

            if self.collide_square(square):
                new_squares.append(square)

        self.squares = new_squares

    def collide_square(self, square):
        explosion_points = []
        new_walls = []
        square_rect = square.get_rect()
        for wall in self.walls:
            if square_rect.intersects(wall.get_rect()):
                explosion_points.append((wall.x, wall.y))
                wall.kill()
            else:
                new_walls.append(wall)

        new_cores = []
        for core in self.cores:
            if core.intersects(square_rect):
                explosion_points.append((core.x, core.y))
                core.kill()
            else:
                new_cores.append(core)
        self.cores = new_cores

        self.walls = new_walls
        if explosion_points:
            square.kill()
            if square.can_cause_big_impact():
                self.make_big_impact()
            explosion_points.append((square.x, square.y))
            self.make_explosion(explosion_points)
            return False
        return True

    def make_explosion(self, points):
        play_explode()
        for x, y in points:
            explosion = Explosion(x, y)
            self.add(explosion, z=5)

    def make_big_impact(self):
        reset_action = MoveTo((self.x, self.y), 0)
        sequence = MoveTo((self.x, self.y), 0)
        for i in xrange(30):
            factor = 30
            if i > 20:
                factor = 40 - i
            sequence += MoveBy((random.uniform(-0.5, 0.5) * factor,
                                random.uniform(-0.5, 0.5) * factor), 0.015)
        sequence += reset_action
        self.do(sequence)

    def get_next_level_class(self):
        return None

    def reset_event_attributes(self):
        self.mouse_position = None
        self.line.visible = False
        self.selected = None

    # Events
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.selected and not self.mouse_position:
            self.line.visible = True
            self.line_action = self.do(Repeat(CallFunc(self.reposition_line)))
        self.mouse_position = (x, y)

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.mouse_position = None
        self.selected = None

        if x > c.OUT_ZONE:
            return

        for i, square in enumerate(self.squares):
            if square.contains(x, y):
                self.selected = square
                return

    def on_mouse_release(self, x, y, buttons, modifiers):
        if not self.selected:
            return

        if self.mouse_position:
            self.remove_action(self.line_action)
            self.shoot()
        else:
            self.squares.remove(self.selected)
            self.split(self.selected)

        self.reset_event_attributes()
