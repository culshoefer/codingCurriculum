#!/usr/bin/env python
import pygame
from pacman.level import Level
from pacman.pacman import Pacman
from pacman.blinky import Blinky
from pacman.pinky import Pinky
from pacman.inky import Inky
from pacman.clyde import Clyde

MAX_FRAMERATE = 30

def same_position(s1, s2):
    return s1.arena_position == s2.arena_position 

if __name__ == '__main__':
    screen_size = (screen_width, screen_height) = (504, 558)
    screen = pygame.display.set_mode(screen_size)
    screen_rect = screen.get_rect()
    
    pygame.mixer.init()
    chomp_sound = pygame.mixer.Sound('sounds/pacman_chomp.wav')
    death_sound = pygame.mixer.Sound('sounds/pacman_death.wav')
    energizer_sound = pygame.mixer.Sound('sounds/pacman_eatfruit.wav')

    l = Level(screen_size, 'levels/level1.png')
    scale_factor = 1.5

    pacman = Pacman(l, 'sprites/pacman.png', scale_factor, 0, 10)

    blinky = Blinky(l, 'sprites/blinky.png', scale_factor, 0, 7)
    pinky = Pinky(l, 'sprites/pinky.png', scale_factor, 0, 6)
    inky = Inky(l, 'sprites/inky.png', scale_factor, 0, 5)
    clyde = Clyde(l, 'sprites/clyde.png', scale_factor, 0, 4)

    players = pygame.sprite.GroupSingle(pacman)
    ghosts = pygame.sprite.Group(blinky, pinky, inky, clyde)

    for ghost in ghosts:
        ghost.follow(pacman)
    
    # Game start
    screen.blit(l.get_surface(), (0, 0))
    l.get_dots().draw(screen)
    players.draw(screen)
    ghosts.draw(screen)
    pygame.display.flip()

    beginning_sound = pygame.mixer.Sound('sounds/pacman_beginning.wav')
    beginning_sound.play()
    pygame.time.wait(int(beginning_sound.get_length() * 1000))

    # Game loop
    clock = pygame.time.Clock()
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

                
        dots = l.get_dots()
        eaten_dot = pygame.sprite.spritecollideany(pacman, dots, same_position)
        if eaten_dot is not None:
            eaten_dot.remove(dots)
            
            if eaten_dot.is_super:
                energizer_sound.play()
                print "You ate an energizer."

            if pygame.mixer.get_busy() == False:
                if eaten_dot.is_super:
                    energizer_sound.play()
                else:
                    chomp_sound.play()

        ghost_collision = pygame.sprite.spritecollideany(pacman, ghosts, pygame.sprite.collide_circle)
        if ghost_collision is not None:
            print "You were eaten by {}.\n".format(ghost_collision.name)

            pygame.mixer.stop()
            death_sound.play()
            pygame.time.wait(int(death_sound.get_length() * 1000))
            pygame.quit()

        # Update in discrete steps
        ticks = clock.tick(MAX_FRAMERATE)

        pacman.time_since_last_update += ticks
        if pacman.time_since_last_update > pacman.get_update_frequency():
            pacman.update()
            pacman.time_since_last_update = 0

        for ghost in ghosts:
            ghost.time_since_last_update += ticks
            if ghost.time_since_last_update > ghost.get_update_frequency():
                ghost.update()
                ghost.time_since_last_update = 0

        # Draw
        screen.blit(l.get_surface(), (0, 0))
        dots.draw(screen)
        players.draw(screen)
        ghosts.draw(screen)
        pygame.display.flip()



