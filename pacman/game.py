#!/usr/bin/env python
import pygame
from pacman.level import Level
from pacman.pacman import Pacman

FRAMES_PER_SECOND = 10
MS_PER_FRAME = (1000.0/FRAMES_PER_SECOND)

def sprites_collide(s1, s2):
    return s1.arena_position == s2.arena_position 

if __name__ == '__main__':
    screen_size = (screen_width, screen_height) = (504, 558)
    screen = pygame.display.set_mode(screen_size)
    screen_rect = screen.get_rect()
    
    pygame.mixer.init()
    chomp_sound = pygame.mixer.Sound('sounds/pacman_chomp.wav')


    l = Level(screen_size, 'levels/level1.png')
    scale_factor = 1.5

    pacman = Pacman(l, 'sprites/pacman.png', scale_factor, (1, 1), 0)
    characters = pygame.sprite.RenderPlain(pacman)

    clock = pygame.time.Clock()
    time_since_last_update = 0
    while True:
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

        # Update in discrete steps
        time_since_last_update += clock.tick(FRAMES_PER_SECOND)

        dots = l.get_dots()
        eaten_dot = pygame.sprite.spritecollideany(pacman, dots, sprites_collide)
        if eaten_dot is not None:
            eaten_dot.remove(dots)
            if pygame.mixer.get_busy() == False:
                chomp_sound.play()

        if time_since_last_update > MS_PER_FRAME:
            characters.update()
            time_since_last_update = 0

        # Draw
        screen.blit(l.get_surface(), (0, 0))
        dots.draw(screen)
        characters.draw(screen)
        pygame.display.flip()



