import pygame
import random
from Entity import Entity

class ShotEngine():
    def __init__(self, gameWidth, gameHeight):
        self.alienShots = []
        self.playerShots = []
        self.previousShotTicks = 0
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight
    
    def isLucky(self, chance):
        return random.random() > chance
    
    def doesAlienShoot(self):
        return self.isLucky(0.997)

    def makeShot(self, x, y, speed):
        shot = Entity(x, y, 0, speed, "img/shot.png", self.gameWidth, self.gameHeight)
        return shot
    
    def addAlienShot(self, x, y):
        shot = self.makeShot(x, y, 0.75)
        self.alienShots.append(shot)

    def deleteAlienShot(self, shot):
        self.alienShots.remove(shot)

    def addPlayerShot(self, shot):
        self.playerShots.append(shot)

    def deletePlayerShot(self, shot):
        self.playerShots.remove(shot)

    def makeRandomShots(self, aliens):
        if(self.doesAlienShoot()):
            row = random.randint(0, 4)
            col = random.randint(0, 10)
            while not aliens[col][row].consider: #skip aliens that are not visible
                row = random.randint(0, 4)
                col = random.randint(0, 10)
            x = aliens[col][row].x
            y = aliens[col][row].y
            self.addAlienShot(x, y)
            
    def considerAlienShot(self, shot, player):
        score = 0
        if player.isHit(shot):
            self.alienShots.remove(shot)
            player.removeLife()
            score += player.score
        return score
        
    def computeAlienShots(self, player):
        score = 0
        for shot in self.alienShots:
            score += self.considerAlienShot(shot, player)
        return score
                
    def considerShotOnSpecialAlien(self, shot, specialAlien):
        if specialAlien.isHit(shot):
            specialAlien.removeLife()
            return specialAlien.score

    def considerPlayerShot(self, shot, specialAlien, aliens):
        score = 0
        specialAlienScore = self.considerShotOnSpecialAlien(shot, specialAlien)
        if specialAlienScore is not None:
            score += specialAlienScore
        for row in aliens:
            for col in row:
                if col.isHit(shot):
                    score += col.score
                    col.removeLife()
                    self.playerShots.remove(shot)
        return score

    def computePlayerShots(self, specialAlien, aliens):
        score = 0
        for shot in self.playerShots:
            playerscore = self.considerPlayerShot(shot, specialAlien, aliens)
            if playerscore is not None:
                score += playerscore
        return score

    def drawPlayerShots(self, screen):
        for shot in self.playerShots:
            if not shot.isInScreen():
                self.playerShots.remove(shot)
            else:
                shot.update()
                shot.draw(screen)
                    
    def drawAlienShots(self, screen):
        for shot in self.alienShots:
            if not shot.isInScreen():
                self.deleteAlienShot(shot)
            else:
                shot.update()
                shot.draw(screen)

    def computeShots(self, player, specialAlien, aliens):
        score = self.computePlayerShots(specialAlien, aliens)
        score += self.computeAlienShots(player)
        return score
                
    def update(self, aliens, screen):
        self.makeRandomShots(aliens)
        self.drawPlayerShots(screen)
        self.drawAlienShots(screen)
