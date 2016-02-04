#!/usr/bin/env python
import pygame
from pacman.level import Level
from pacman.pacman import Pacman
from pacman.ghost import Ghost

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
    death_sound = pygame.mixer.Sound('sounds/pacman_death.wav')

    l = Level(screen_size, 'levels/level1.png')
    scale_factor = 1.5

    pacman = Pacman(l, 'sprites/pacman.png', scale_factor, 0)
    red_ghost = Ghost(l, 'sprites/red_ghost.png', scale_factor, 0)

    red_ghost.follow(pacman)

    ghosts = pygame.sprite.Group(red_ghost)
    characters = pygame.sprite.Group(pacman, red_ghost)
    
    # Game start
    screen.blit(l.get_surface(), (0, 0))
    l.get_dots().draw(screen)
    characters.draw(screen)
    pygame.display.flip()

    beginning_sound = pygame.mixer.Sound('sounds/pacman_beginning.wav')
    beginning_sound.play()
    pygame.time.wait(int(beginning_sound.get_length() * 1000))

    # Game loop
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

        if pygame.sprite.spritecollideany(pacman, ghosts, sprites_collide):
            print "You were eaten.\n"
            if pygame.mixer.get_busy() == False:
                death_sound.play()
                pygame.time.wait(int(death_sound.get_length() * 1000))
                pygame.quit()

        if time_since_last_update > MS_PER_FRAME:
            characters.update()
            time_since_last_update = 0


        # Draw
        screen.blit(l.get_surface(), (0, 0))
        dots.draw(screen)
        characters.draw(screen)
        pygame.display.flip()



