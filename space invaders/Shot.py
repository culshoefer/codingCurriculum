from Entity import Entity
white = 255, 255, 255
black = 0, 0, 0

class Shot(Entity):
    def __init__(self, x, y, dx, dy, gameWidth, gameHeight):
        super(Shot, self).__init__(x, y, dx, dy, "img/shot.png", gameWidth, gameHeight)