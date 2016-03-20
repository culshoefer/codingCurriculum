import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, image, gameWidth, gameHeight):
b        super(Entity, self).__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.image = pygame.image.load(image)
        self.width = self.image.get_width()
        self.height= self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.posBoundaryLeft = 20 + self.width/2
        self.posBoundaryRight= gameWidth - (20 + self.width/2)
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
            self.dx = - self.dx
        if self.x > self.posBoundaryRight:
            self.x = self.posBoundaryRight
            self.dx = -self.dx
    
    def isInScreen(self):
        return not(self.y > self.gameHeight or self.y < 0 or self.x > self.gameWidth or self.x < 0)

    def isHit(self, entity):
        return self.consider and entity.consider and self.intersects(entity)
        
    def draw(self, screen):
        if self.consider and self.isInScreen():
            screen.blit(self.image, self.rect)

