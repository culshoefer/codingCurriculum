import pygame
from Entity import Entity
class AliveEntity(Entity):
    def __init__(self, score, x, y, dx, dy, image, lives, gameWidth, gameHeight):
        super(AliveEntity, self).__init__(x, y, dx, dy, image, gameWidth, gameHeight)
        self.score = score
        self.lives = lives

    def update(self):
        self.checkBoundaries()
        self.rect.center = (self.x, self.y)
        if not self.isInScreen() or self.lives <= 0:
            self.consider = False

    def updateWithMove(self):
        self.update()
        self.move()
        
    def removeLife(self):
        self.lives -= 1
