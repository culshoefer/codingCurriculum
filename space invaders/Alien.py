import pygame
from AliveEntity import AliveEntity

class Alien(AliveEntity):
    def __init__(self, score, x, y, dx, dy, image, lives, gameWidth, gameHeight):
        super(Alien, self).__init__(score, x, y, dx, dy, image, lives, gameWidth, gameHeight)
        self.consider = True

    def draw(self, screen):
        if self.consider:
            if not self.isInScreen():
                self.consider = False
            screen.blit(self.image, self.rect)
    
    
