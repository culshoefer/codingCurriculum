import pygame
import random
from Entity import Entity
from AliveEntity import AliveEntity
from ShotEngine import ShotEngine
from Display import Display

white = 255, 255, 255
black = 0, 0, 0

class Game():
    def __init__(self, startScore, aliens, player, width, height, size):
        self.score = startScore
        self.display = Display()
        self.shotEngine = ShotEngine(width, height)
        self.ticks = 0
        self.player= player
        self.aliens= aliens
        self.specialAlien = AliveEntity(0, 0, 0, 0, 0, "img/shot.png", 0, width, height) #dummy assignment
        self.specialAlien.consider = False
        self.running = True
        self.aliensExist = True
        self.screen = pygame.display.set_mode(size)
        self.width = width
        self.height = height
        
    def addScore(self, toAdd):
        self.score = self.score + toAdd
    
    def isLucky(self, chance):
        return random.random() > chance
        
    def spawnSpecialAlien(self):
        print("SPECIALALIEN")
        self.specialAlien = AliveEntity(100, 100, 90, 2, 0, "img/sprite8.png", 1, self.width, self.height)
        self.specialAlien.posBoundaryRight = self.width + 40
        
    def checkGameStop(self, event):
        if event.type == pygame.QUIT: 
            self.running = False

    def computeInput(self):
        for event in pygame.event.get():
            self.checkGameStop(event)
        pressed_keys = pygame.key.get_pressed()
        self.player.checkKeyboardInput(pressed_keys)
        shot = self.player.checkShoot(pressed_keys, self.ticks)
        if shot is not None:
            self.shotEngine.addPlayerShot(shot)

    def drawSpecialAlien(self):
        if self.specialAlien.consider:
            self.specialAlien.update()
            self.screen.blit(self.specialAlien.image, self.specialAlien.rect)
    
    def drawAlien(self, alien):
        if self.ticks % 200 == 0:
            alien.update()
        alien.draw(self.screen) 
        
    def drawAliens(self):
        self.aliensExist = False
        self.drawSpecialAlien()
        for row in self.aliens:
            for col in row:
                if col is not None:
                    self.aliensExist = True
                    self.drawAlien(col)

    def update(self):
        self.display.drawAll(self.screen, self.score, self.player.lives)
        self.computeInput()
        self.player.update()
        self.player.draw(self.screen)
        self.drawAliens()
        self.shotEngine.update(self.aliens, self.screen)
        self.score += self.shotEngine.computeShots(self.player, self.specialAlien, self.aliens)
        self.ticks += 1
        if(self.isLucky(0.99999)):
            self.spawnSpecialAlien()
        if self.isGameOver():
            self.running = False

    def isGameOver(self):
        return self.player.lives == 0 or not self.aliensExist

    def isRunning(self):
        return self.running
