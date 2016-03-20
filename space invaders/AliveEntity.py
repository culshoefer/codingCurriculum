import pygame
from Entity import Entity
class AliveEntity(Entity):
    def __init__(self, score, x, y, dx, dy, image, lives, gameWidth, gameHeight):
        super(AliveEntity, self).__init__(x, y, dx, dy, image, gameWidth, gameHeight)
        self.score = score
        self.image = pygame.image.load(image)
        self.width = self.image.get_width()
        self.height= self.image.get_height()
        self.rect = self.image.get_rect()
        self.lives = lives
