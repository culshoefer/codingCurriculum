#!/usr/bin/env python
import pygame
from pacman.level import Level
from pacman.character import Character

FRAMES_PER_SECOND = 30

if __name__ == '__main__':
    screen_size = (screen_width, screen_height) = (600, 660)
    screen = pygame.display.set_mode(screen_size)
    screen_rect = screen.get_rect()

    l = Level(screen_size, 'levels/level1.png')
    
    pacman = Character(l, 'sprites/pacman.png', (2,2), 0)
    characters = pygame.sprite.RenderPlain(pacman)

    clock = pygame.time.Clock()

    while True:
        deltat = clock.tick(FRAMES_PER_SECOND)

        # Process events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pacman.set_direction(0)
                if event.key == pygame.K_UP:
                    pacman.set_direction(1)
                if event.key == pygame.K_LEFT:
                    pacman.set_direction(2) 
                if event.key == pygame.K_DOWN:
                    pacman.set_direction(3) 

        # Update
        characters.update(deltat)
        
        # Draw
        screen.blit(l.get_surface(), (0,0))
        characters.draw(screen)
        pygame.display.flip()

