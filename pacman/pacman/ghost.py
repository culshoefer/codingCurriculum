import pygame
from .character import Character, NUM_DIRECTIONS
import random

NUM_MODES = 3
CHASE_MODE = 0
SCATTER_MODE = 1
FRIGHTENED_MODE = 2

class Ghost(Character):
    target = None

    def _bfs(self, starting_point, target):
        visited = [starting_point]
        to_visit = [[starting_point]]

        found_target = False
        while len(to_visit) > 0 and not found_target:
            path = to_visit.pop(0)

            node = path[-1]

            if node == target:
                found_target = True
                return path

            # Visit all accessible neighbours
            for dir in range(NUM_DIRECTIONS):
                next = self.level.get_next_cell_in_direction(node, dir)
                if self.level.is_accessible(next) and next not in visited:
                    new_path = list(path)
                    new_path.append(next)
                    to_visit.append(new_path)
                    visited.append(next)

        return None

    def _direction_to(self, target_pos):
        path_to_target = self._bfs(self.arena_position, self.target.arena_position)

        if path_to_target is not None and len(path_to_target) >= 2:
            next_cell = path_to_target[1]

            diff = (next_cell[0] - self.arena_position[0], next_cell[1] - self.arena_position[1])
            diff_to_direction = {(0, 1): 0, (-1, 0): 1, (0, -1): 2, (1, 0): 3}

            return diff_to_direction[diff]

        else:
            return self.curr_direction

    def follow(self, target):
        self.target = target

    def update(self):
        if self.level.is_turning_point(self.arena_position):
            self.curr_direction = self._direction_to(self.target.arena_position)

        next_cell = self.get_next_cell_in_direction(self.curr_direction)
        if self.level.is_accessible(next_cell):
            self.arena_position = next_cell
            self.rect = self.image.get_rect().move(self.level.get_position_from_arena_position(self.arena_position))
