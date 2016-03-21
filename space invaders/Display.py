import pygame
import copy

topDist = 150
liveXDist = 30
white = 255, 255, 255
black = 0, 0, 0

class Display():
    def __init__(self):
        self.lifeImage = pygame.image.load("img/heart.png")
        self.font = pygame.font.SysFont("monospace", 20)
        self.text = self.font.render("SCORE", 1, white)
        self.textpos = self.text.get_rect()
        self.textpos.x = 20
        self.textpos.y = 30
        self.scorepos = copy.copy(self.textpos)
        self.scorepos.x = self.scorepos.x + self.text.get_width() + 20
        self.scorepos.y = self.scorepos.y

    def drawAll(self, screen, score, numLives):
        self.drawAllText(screen, score)
        self.drawLives(screen, numLives)

    def drawAllText(self, screen, score):
        screen.fill(black)
        screen.blit(self.font.render(`score`, 30, white), self.scorepos)
        screen.blit(self.text, self.textpos)

    def drawLives(self, screen, numLives):
        for i in range(numLives):
            livesRect = self.lifeImage.get_rect()
            livesRect.x = self.textpos.x + topDist + i * liveXDist
            livesRect.y = self.textpos.y
            screen.blit(self.lifeImage, livesRect)
    
