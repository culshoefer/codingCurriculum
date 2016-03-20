import pygame
from AliveEntity import AliveEntity
from Shot import Shot

class Player(AliveEntity):
    def __init__(self, score, lives, gameWidth, gameHeight):
        super(Player, self).__init__(score, gameWidth/2, 400, 0, 0, "img/player.png", lives, gameWidth, gameHeight)
        self.lives = lives
        self.last_shot = 0
        
    def shoot(self, ticks):
        shot = Shot(self.x, self.y, 0, -1.25, self.gameWidth, self.gameHeight)
        self.last_shot = ticks
        return shot

    def checkKeyboardInput(self, pressed_keys):
        self.checkGoLeft(pressed_keys)
        self.checkGoRight(pressed_keys)
        
    def checkShoot(self, pressed_keys, ticks):
        shot = None
        if pressed_keys[pygame.K_SPACE] and ticks > self.last_shot + 200:
            shot = self.shoot(ticks)
        return shot

    def checkGoLeft(self, pressed_keys):
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.dx = -1
            
    def checkGoRight(self, pressed_keys):
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.dx = 1
            
    def removeLife(self):
        self.lives -= 1

    def update(self):
        self.move()
        self.checkBoundaries()
        self.rect.center = (self.x, self.y)
        self.dx = 0
        
