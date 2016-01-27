#!/usr/bin/env python
import pygame
from pacman.level import Level

if __name__ == '__main__':
    l = Level('levels/level1.png')

    size = (screen_width, screen_height) = (600, 660)
    screen = pygame.display.set_mode(size)

    while True:
        screen.blit(l.get_surface(screen_width, screen_height), (0,0))
        pygame.display.flip()

        pygame.time.wait(10)

