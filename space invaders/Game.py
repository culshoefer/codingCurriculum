import pygame
import copy
import random
from Entity import Entity

white = 255, 255, 255
black = 0, 0, 0

class Game():
    def __init__(self, startScore, lifeImage, aliens, player, width, height, size):
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
        self.specialAlien = Entity(0, 0, 0, "img/shot.png", 0, width, height)
        self.specialAlien.consider = False
        self.playerShots = []
        self.alienShots = []
        self.running = True
        self.aliensExist = True
        self.screen = pygame.display.set_mode(size)
        self.width = width
        self.height = height
        
    def addScore(self, toAdd):
        self.score = self.score + toAdd
    
    def isLucky(self, chance):
        return random.random() > chance
    
    def makeRandomShots(self):
        if(self.isLucky(0.997)):
            row = random.randint(0, 4)
            col = random.randint(0, 10)
            while not self.aliens[col][row].consider: #skip aliens that are not visible
                row = random.randint(0, 4)
                col = random.randint(0, 10)
            shot = self.makeShot(self.aliens[col][row].x, self.aliens[col][row].y, 0.75)
            self.alienShots.append(shot)
    
    def spawnSpecialAlien(self):
        print("SPECIALALIEN")
        self.specialAlien = Entity(100, 100, 90, "img/sprite8.png", 1, self.width, self.height)
        self.specialAlien.setIntervalX(2)
        self.specialAlien.posBoundaryRight = self.width + 40

    def makeShot(self, x, y, speed):
        shot = Entity(0, x, y, "img/shot.png", 1, self.width, self.height)
        shot.setIntervalX(0)
        shot.setIntervalY(speed)
        return shot
        
    def checkGameStop(self, event):
        if event.type == pygame.QUIT: 
            self.running = False

    def checkGoLeft(self, pressed_keys):
        if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:
            self.player.setIntervalX(-1)
            
    def checkGoRight(self, pressed_keys):
        if pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:
            self.player.setIntervalX(1)
           
    def isPauseBetweenShotsBig(self):
        return self.ticks - 200 > self.lastShot

    def computeInput(self):
        for event in pygame.event.get():
            self.checkGameStop(event)
        pressed_keys = pygame.key.get_pressed()
        self.checkGoLeft(pressed_keys)
        self.checkGoRight(pressed_keys)
        if pressed_keys[pygame.K_SPACE] and self.isPauseBetweenShotsBig():
            shot = self.makeShot(self.player.x, self.player.y, -1.25)
            self.playerShots.append(shot)
            self.lastShot = self.ticks

    def drawAllText(self):
        self.screen.fill(black)
        self.screen.blit(self.font.render(`self.score`, 30, white), self.scorepos)
        self.screen.blit(self.text, self.textpos)

    def drawSpecialAlien(self):
        if self.specialAlien.consider:
            self.specialAlien.update()
            if not self.specialAlien.isInScreen():
                self.specialAlien.consider = False
            self.screen.blit(self.specialAlien.image, self.specialAlien.rect)
    
    def drawAlien(self, alien):
        if self.ticks % 200 == 0:
            alien.update()
        self.screen.blit(alien.image, alien.rect)
        
    def drawLives(self):
        for i in range(0, self.player.lives):
            livesRect = self.lifeImage.get_rect()
            livesRect.x = self.textpos.x + 150 + i * 30
            livesRect.y = self.textpos.y
            self.screen.blit(self.lifeImage, livesRect)

    def drawAliens(self):
        self.aliensExist = False
        self.drawSpecialAlien()
        for row in self.aliens:
            for col in row:
                if col is not None and col.consider:
                    self.aliensExist = True
                    self.drawAlien(col)

    def considerAlienShot(self, shot):
        if self.player.isHit(shot):
            self.alienShots.remove(shot)
            self.player.removeLife()
            self.addScore(self.player.score)
        
    def computeAlienShots(self):
        for shot in self.alienShots:
            if not shot.isInScreen():
                self.alienShots.remove(shot)
                continue
            else:
                shot.update()
                self.screen.blit(shot.image, shot.rect)
                self.considerAlienShot(shot)
    
    def considerPlayerShot(self, shot):
        if self.specialAlien.isHit(shot):
            self.addScore(self.specialAlien.score)
            self.specialAlien.consider = False
        for row in self.aliens:
            for col in row:
                if col.isHit(shot):
                    self.addScore(col.score)
                    col.consider = False
                    self.playerShots.remove(shot)

    def computePlayerShots(self):
        for shot in self.playerShots:
            if not shot.isInScreen():
                self.playerShots.remove(shot)
            else:
                shot.update()
                self.screen.blit(shot.image, shot.rect)
                self.considerPlayerShot(shot)

    def isGameOver(self):
        return self.player.lives == 0 or not self.aliensExist

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
        self.drawLives()
        if self.isGameOver():
            self.running = False
        self.ticks += 1
        if(self.isLucky(0.9999)):
            self.spawnSpecialAlien()

    def isRunning(self):
        return self.running
