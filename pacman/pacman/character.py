import pygame
from .level import Level

class Character(pygame.sprite.Sprite):
    image = None
    rect = None
    direction = None #right = 0, up = 1, left = 2, down = 3
    arena_position = None #(row, col)

    def __init__(self, level, image, arena_position, direction):
        pygame.sprite.Sprite.__init__(self)

        self.level = level

        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotate(self.image, direction * 90)
        self.direction = direction

        self.arena_position = arena_position
        self.rect = self.image.get_rect().move(level.get_position_from_arena_position(arena_position))

    def set_direction(self, direction):
        assert direction in range(4), "pacman.character: tried to set invalid direction {}.\n".format(direction)


        self.image = pygame.transform.rotate(self.image, (direction - self.direction) * 90)
        self.direction = direction

    def update(self, deltat):
        if deltat > 100:
            arena_row, arena_col = self.arena_position

            assert self.direction in range(4), "pacman.character: direction is {}, which is invalid.\n".format(self.direction)

            if (self.direction == 0) and self.level.is_accesible((arena_row, arena_col+1)):
                arena_col += 1
            elif self.direction == 1 and self.level.is_accesible((arena_row-1, arena_col)):
                arena_row -= 1
            elif self.direction == 2 and self.level.is_accesible((arena_row, arena_col-1)):
                arena_col -= 1
            elif self.direction == 3 and self.level.is_accesible((arena_row+1, arena_col)):
                arena_row += 1

            self.arena_position = (arena_row, arena_col)
            self.rect = self.image.get_rect().move(self.level.get_position_from_arena_position(self.arena_position))







