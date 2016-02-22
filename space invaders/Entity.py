import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, score, x, y, image, lives, gameWidth, gameHeight):
        super(Entity, self).__init__()
        self.score = score
        self.x = x
        self.y = y
        self.dx = 4
        self.dy = 0
        self.image = pygame.image.load(image)
        self.width = self.image.get_width()
        self.height= self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.posBoundaryLeft = 20 + self.width/2
        self.posBoundaryRight= gameWidth - (20 + self.width/2)
        self.lives = lives
        self.consider = True
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
        
    def update(self):
        self.move()
        self.checkBoundaries()
        self.rect.center = (self.x, self.y)
                 
    def intersects(self, Entity):
        return self.rect.colliderect(Entity.rect)
    
    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def checkBoundaries(self):
        if self.x < self.posBoundaryLeft:
            self.x = self.posBoundaryLeft
            self.setIntervalX(4)
        if self.x > self.posBoundaryRight:
            self.x = self.posBoundaryRight
            self.setIntervalX(-4)

    def setIntervalX(self, newInterval):
        self.dx = newInterval

    def setIntervalY(self, newInterval):
        self.dy = newInterval
        
    def setPosition(self, x, y):
        self.x = x
        self.y = y

    def removeLife(self):
        self.lives = self.lives - 1
    
    def isInScreen(self):
        return not(self.y > self.gameHeight or self.y < 0 or self.x > self.gameWidth or self.x < 0)

    def isHit(self, entity):
        return self.consider and entity.consider and self.intersects(entity)
