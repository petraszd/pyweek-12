from squarescity.levels import Level
from squarescity.squares import BigSquare, MiddleSquare, SmallSquare
from squarescity.cores import Core


class Level1(Level):

    def create_squares(self):
        return [MiddleSquare((200, 200)),
                MiddleSquare((200, 400))]

    def create_cores(self):
        return [Core((950, 250))]

    def get_next_level_class(self):
        return Level2


class Level2(Level):

    def create_squares(self):
        return [BigSquare((200, 300))]

    def create_cores(self):
        return [Core((950, 250))]

    def walls_positions(self):
        return [(870, 210), (870, 230), (870, 250),
                (870, 270), (870, 290), (870, 310),
                (850, 210), (850, 230), (850, 250),
                (850, 270), (850, 290), (850, 310)]

    def get_next_level_class(self):
        return Level3


class Level3(Level):

    def create_squares(self):
        return [SmallSquare((200, 150)),
                SmallSquare((200, 300)),
                SmallSquare((200, 450))]

    def create_cores(self):
        return [Core((950, 100)),
                Core((950, 500))]

    def get_next_level_class(self):
        return Level4


class Level4(Level):

    def create_squares(self):
        return [BigSquare((200, 300))]

    def create_cores(self):
        return [Core((950, 300))]

    def walls_positions(self):
        return [(650, y) for y in xrange(80, 600, 80)] + \
               [(750, y) for y in xrange(40, 600, 40)] + \
               [(870, y) for y in xrange(240, 380, 20)]

    def get_next_level_class(self):
        return Level5


class Level5(Level):

    def create_squares(self):
        return [MiddleSquare((200, 300))]

    def create_cores(self):
        return [Core((880, 300))]

    def walls_positions(self):
        return [(640, y) for y in xrange(230, 790, 20)] + \
               [(660, y) for y in xrange(230, 790, 20)] + \
               [(680, y) for y in xrange(230, 790, 20)]
