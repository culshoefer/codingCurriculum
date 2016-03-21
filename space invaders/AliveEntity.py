import pygame
from Entity import Entity
class AliveEntity(Entity):
    def __init__(self, score, x, y, dx, dy, image, lives, gameWidth, gameHeight):
        super(AliveEntity, self).__init__(x, y, dx, dy, image, gameWidth, gameHeight)
        self.score = score
        self.lives = lives
