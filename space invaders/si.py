import pygame
import sys
import random


pygame.init()
size = width, height = 448, 512
black = 0, 0, 0

class Entity(pygame.sprite.Sprite):
    def __init__(self, lives, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.dx = 4
        self.dy = 0
        self.img = pygame.Surface([0, 0])
        self.img = pygame.image.load(img)
        self.width = self.img.get_width()
        self.height= self.img.get_height()
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.posBoundaryLeft = 20 + self.width/2
        self.posBoundaryRight= width - (20 + self.width/2)
        self.width = self.img.get_width()
        self.height= self.img.get_height()
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.lives = lives
        
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

class Game():
    def __init__(self, startScore, lifeImage, player, aliens):
        self.lifeImage = pygame.image.load(lifeImage)
        self.font = pygame.font.SysFont("monospace", 20)
        self.text = self.font.render("SCORE", 1, (255, 255, 255))
        self.textpos = self.text.get_rect()
        self.textpos.x = 20
        self.textpos.y = 30
        self.score = startScore
        self.ticks = 0
        self.player= player
        self.lastShot = self.ticks
        self.aliens= aliens
        self.playerShots = []
        self.alienShots = []
        self.running = True
        self.screen = pygame.display.set_mode(size)
        
    def addScore(self, toAdd):
        self.score = self.score + toAdd


    def makeRandomShots(self):
        if(random.random() > 0.997):
            row = random.randint(0, 4)
            col = random.randint(0, 10)
            self.alienShots.append(Entity(1, self.aliens[col][row].x, self.aliens[col][row].y, "shot.png"))
            self.alienShots[-1].setIntervalX(0)
            self.alienShots[-1].setIntervalY(0.75)

    def computeInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game.running = False
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.player.setIntervalX(-0.5)
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.player.setIntervalX(0.5)
        if pressed_keys[pygame.K_SPACE] and self.ticks - 200 > self.lastShot:
            self.playerShots.append(Entity(1, self.player.x, self.player.y, "shot.png"))
            self.playerShots[-1].setIntervalX(0)
            self.playerShots[-1].setIntervalY(-1)
            self.lastShot = self.ticks
            
    def update(self):
        self.screen.fill(black)
        self.screen.blit(self.text, self.textpos)
        self.computeInput()
        self.player.update()
        self.screen.blit(self.player.img, self.player.rect)
        self.player.setIntervalX(0)
        self.makeRandomShots()
        for row in self.aliens:
            for col in row:
                if self.ticks % 300 == 0:
                    col.update()
                self.screen.blit(col.img, col.rect)
        for shot in self.alienShots:
            if shot.y > height or shot.y < 0:
                self.alienShots.remove(shot)
                continue
            shot.update()
            self.screen.blit(shot.img, shot.rect)
            if self.player.intersects(shot):
                self.alienShots.remove(shot)
                self.player.removeLife()
        for shot in self.playerShots:
            if shot.y > height or shot.y < 0:
                self.playerShots.remove(shot)
                continue
            shot.update()
            self.screen.blit(shot.img, shot.rect)
            for row in self.aliens:
                for col in row:
                    if shot.intersects(col):
                        #self.aliens.remove(col)
                        self.playerShots.remove(shot)
        if self.player.lives == 0:
            self.running = False
        self.ticks += 1
        #self.sprites.update()
        #self.sprites.draw()
        for i in range(0, self.player.lives):
            livesRect = self.lifeImage.get_rect()
            livesRect.x = self.textpos.x + 150 + i * 30
            livesRect.y = self.textpos.y
            self.screen.blit(self.lifeImage, livesRect)
			
    def isRunning(self):
        return self.running
	
aliens = []
for i in range(11):
    new = []
    for j in range(5):
        newAlien = Entity(1, width/2 -1400 + 30 * i, height/2 - 130 + 30 * j, "sprite" + str(j+1) + ".png")
        newAlien.posBoundaryLeft = 50 + 30 * i
        newAlien.posBoundaryRight= width -50 - 30 * (10 - i)
        new.append(newAlien)
    aliens.append(new)
player = Entity(3, width/2, 400, "player.png")
game = Game(0, "heart.png", player, aliens)
#game.sprites.add(player)
#for row in aliens:
#    for column in row:
#        game.sprites.add(column)

while game.isRunning():
    game.update()
    pygame.display.flip()

pygame.quit()
#todo:  Remove aliens that are hit by shots
#       Add barriers
#       Add score system
#       Add animations
    



    
