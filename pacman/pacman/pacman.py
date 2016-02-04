import pygame
from .level import GHOST_ONLY_BLOCK
from .character import Character, ROTATION_ANGLE


class Pacman(Character):
    def __init__(self, level, image, scale_factor, direction):
        arena_position = level.get_pacman_spawn_position()
        Character.__init__(self, level, image, scale_factor, arena_position, direction)

    def is_accessible(self, arena_position):
        arena_row, arena_col = arena_position
        is_ghost_only_block = self.level.arena[arena_row][arena_col] == GHOST_ONLY_BLOCK

        return self.level.is_accessible(arena_position) and (not is_ghost_only_block)

    def update_direction(self):
        if self.next_direction is not None and self.is_accessible(self.get_next_cell_in_direction(self.next_direction)):
            self.image = pygame.transform.rotate(self.image, (self.next_direction - self.curr_direction) * ROTATION_ANGLE)

            self.curr_direction = self.next_direction
            self.next_direction = None

    def update(self):
        self.update_direction()
        next_cell = self.get_next_cell_in_direction(self.curr_direction)

        if self.is_accessible(next_cell):
            self.arena_position = next_cell
            self.rect = self.image.get_rect().move(self.level.get_position_from_arena_position(self.arena_position))
