import pygame
import sys
pygame.init()

size = width, height = 448, 512
speed = [2, 2]
black = 0, 0, 0

class Entity(pygame.sprite.Sprite):
    def __init__(self, lives, x, y, img, altimg):
        pygame.sprite.Sprite.__init__(self)
        self.moveDelay = 0
        self.x = x
        self.y = y
        self.dx= 1
        self.img = pygame.Surface([0, 0])
        self.img = pygame.image.load(img)
        self.altimg = pygame.image.load(altimg)
        self.width = self.img.get_width()
        self.height= self.img.get_height()
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.posBoundaryLeft = self.width/2
        self.posBoundaryRight= width - self.width/2
        self.width = self.img.get_width()
        self.height= self.img.get_height()
        self.posBoundaryLeft = self.width/2
        self.posBoundaryRight= width - self.width/2
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.entities = pygame.sprite.Group()
        self.lives = lives
        
    def update(self):
        self.move()
        self.checkBoundaries()
        self.rect.center = (self.x, self.y)
        self.setInterval(0)
        pygame.display.update()
                 
    def intersects(self, Entity):
        return self.rect.colliderect(Entity.rect)
    
    def move(self):
        self.x = self.x + self.dx

    def checkBoundaries(self):
        if self.x < self.posBoundaryLeft:
            self.x = self.posBoundaryLeft
        if self.x > self.posBoundaryRight:
            self.x = self.posBoundaryRight
        
    def setMoveDelay(self, moveDelay):
        self.moveDelay = moveDelay

    def setInterval(self, newInterval):
        self.dx = newInterval
        
    def setPosition(self, x, y):
        self.x = x
        self.y = y

class Game():
    def __init__(self, startScore, lifeImage, lives, player):
        self.lifeImage = pygame.image.load(lifeImage)
        self.font = pygame.font.SysFont("monospace", 20)
        self.text = self.font.render("SCORE", 1, (255, 255, 255))
        self.textpos = self.text.get_rect()
        self.textpos.x = 20
        self.textpos.y = 30
        self.score = startScore
        self.ticks = 0
        self.lives = lives
        self.player= player
        self.running = True
        self.screen = pygame.display.set_mode(size)
        
    def addScore(self, toAdd):
        self.score = self.score + toAdd

    def removeLife(self):
        self.lives = self.lives - 1
        if self.lives == 0:
            self.running = False

    def update(self):
        self.screen.fill(black)
        self.screen.blit(self.text, self.textpos)
        self.screen.blit(self.player.img, self.player.rect)

        for i in range(0, self.lives -1):
            livesRect = self.lifeImage.get_rect()
            livesRect.x = self.textpos.x + 200 + i * 30
            livesRect.y = self.textpos.y + 200 + i * 30
            pygame.display.update()
			
    def isRunning(self):
        return self.running
	
	


player = Entity(3, width/2, 400, "player.png")
game = Game(0, "heart.jpg", 3, player)

running = True
while game.isRunning():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: game.running = False
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
        game.player.setInterval(-1)
    if (pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]):
        game.player.setInterval(1)
    player.update()
    game.update()
    pygame.display.flip()


pygame.quit()
#11x5 enemies
#fire stuff randomly
#fire randomly every 30 seconds
#enemies[]

#class menu:
#    start game
#    high score
#class highscore:
#    rankInHS
    
#class Entity:
#    width, height, position
#    image
#    points
#    damage received
#class mover:
#    move around
#    fire
    



    
