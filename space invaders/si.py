import pygame
import sys
import random
import copy


class Entity(pygame.sprite.Sprite):
    def __init__(self, lives, x, y, image, score):
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
        self.posBoundaryRight= width - (20 + self.width/2)
        self.lives = lives
        self.consider = True
        
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
    def __init__(self, startScore, lifeImage, aliens, player):
        self.lifeImage = pygame.image.load(lifeImage)
        self.font = pygame.font.SysFont("monospace", 20)
        self.text = self.font.render("SCORE", 1, white)
        self.textpos = self.text.get_rect()
        self.textpos.x = 20
        self.textpos.y = 30
        self.score = startScore
        self.scorepos = copy.copy(self.textpos)
        self.scorepos.x = self.scorepos.x + self.text.get_width() + 20
        self.scorepos.y = self.scorepos.y
        self.ticks = 0
        self.player= player
        self.lastShot = self.ticks
        self.aliens= aliens
        self.specialAlien = Entity(0, 0, 0, "shot.png", 0)
        self.specialAlien.consider = False
        self.playerShots = []
        self.alienShots = []
        self.running = True
        self.aliensExist = True
        self.screen = pygame.display.set_mode(size)
        
    def addScore(self, toAdd):
        self.score = self.score + toAdd


    def makeRandomShots(self):
        if(random.random() > 0.997):
            row = random.randint(0, 4)
            col = random.randint(0, 10)
            while not self.aliens[col][row].consider:
                row = random.randint(0, 4)
                col = random.randint(0, 10)
            self.alienShots.append(Entity(1, self.aliens[col][row].x, self.aliens[col][row].y, "shot.png", 0))
            self.alienShots[-1].setIntervalX(0)
            self.alienShots[-1].setIntervalY(0.75)

    def computeInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game.running = False
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.player.setIntervalX(-1)
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.player.setIntervalX(1)
        if pressed_keys[pygame.K_SPACE] and self.ticks - 200 > self.lastShot:
            self.playerShots.append(Entity(1, self.player.x, self.player.y, "shot.png", 0))
            self.playerShots[-1].setIntervalX(0)
            self.playerShots[-1].setIntervalY(-1.25)
            self.lastShot = self.ticks

    def drawAllText(self):
        self.screen.fill(black)
        self.screen.blit(self.font.render(`self.score`, 30, white), self.scorepos)
        self.screen.blit(self.text, self.textpos)

    def drawAliens(self):
        self.aliensExist = False
        if self.specialAlien.consider:
            self.specialAlien.update()
            if self.specialAlien.rect.x > width:
                self.specialAlien.consider = False
            self.screen.blit(self.specialAlien.image, self.specialAlien.rect)
        for row in self.aliens:
            for col in row:
                if col.consider:
                    self.aliensExist = True
                    if self.ticks % 200 == 0:
                        col.update()
                    self.screen.blit(col.image, col.rect)

    def computeAlienShots(self):
        for shot in self.alienShots:
            if shot.y > height or shot.y < 0:
                self.alienShots.remove(shot)
                continue
            shot.update()
            self.screen.blit(shot.image, shot.rect)
            if self.player.intersects(shot):
                self.alienShots.remove(shot)
                self.player.removeLife()
                self.addScore(self.player.score)

                
    def computePlayerShots(self):
        for shot in self.playerShots:
            if shot.y > height or shot.y < 0:
                self.playerShots.remove(shot)
                continue
            shot.update()
            self.screen.blit(shot.image, shot.rect)
            if self.specialAlien.consider and shot.intersects(self.specialAlien):
                self.addScore(self.specialAlien.score)
                self.specialAlien.consider = False
            for row in self.aliens:
                for col in row:
                    if col.consider and shot.intersects(col):
                        self.addScore(col.score)
                        print(`col.score`)
                        col.consider = False
                        self.playerShots.remove(shot)
                
    def update(self):
        self.drawAllText()
        self.computeInput()
        self.player.update()
        self.screen.blit(self.player.image, self.player.rect)
        self.drawAliens()
        self.player.setIntervalX(0)
        self.makeRandomShots()
        self.computeAlienShots()
        self.computePlayerShots()
        if self.player.lives == 0 or not self.aliensExist:
            self.running = False
        self.ticks += 1
        for i in range(0, self.player.lives):
            livesRect = self.lifeImage.get_rect()
            livesRect.x = self.textpos.x + 150 + i * 30
            livesRect.y = self.textpos.y
            self.screen.blit(self.lifeImage, livesRect)
        if(random.random() > 0.9999):
            print("SPECIALALIEN")
            self.specialAlien = Entity(1, 100, 90, "sprite8.png", 100)
            self.specialAlien.setIntervalX(2)
            self.specialAlien.posBoundaryRight = width + 40
    def isRunning(self):
        return self.running


pygame.init()
size = width, height = 448, 512
black = 0, 0, 0
white = 255, 255, 255

aliens = []
clock = pygame.time.Clock()
for i in range(11):
    new = []
    for j in range(5):
        x = width/2 -1400 + 30 * i
        y = height/2 - 130 + 30 * j
        newAlien = Entity(1, x, y, "sprite" + str(j+1) + ".png", 5 * (6 - j))
        newAlien.posBoundaryLeft = 50 + 30 * i
        newAlien.posBoundaryRight= width -50 - 30 * (10 - i)
        new.append(newAlien)
    aliens.append(new)
player = Entity(3, width/2, 400, "player.png", -100)
game = Game(0, "heart.png", aliens, player)
#game.sprites.add(player)
#for row in aliens:
#    for column in row:
#        game.sprites.add(column)

while game.isRunning():
    game.update()
    pygame.display.flip()
    clock.tick(300)

print("END")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: break
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_SPACE]:
        break
    if not game.aliensExist:
        text = game.font.render("YOU WON!", 1, white)
    else:
        text = game.font.render("YOU LOST.", 1, white)        
    textRect = text.get_rect()
    textRect.x = width/2
    textRect.y = height/2
    game.screen.blit(text, textRect)
    pygame.display.flip()
    clock.tick(300)
    
pygame.quit()
#todo:  Remove aliens that are hit by shots
#       Add barriers
#       Add score system
#       Add animations
    



    
