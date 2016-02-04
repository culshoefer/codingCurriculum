import pygame
from .character import Character, NUM_DIRECTIONS


class Ghost(Character):
    target = None

    def __init__(self, level, image, scale_factor, direction):
        arena_position = level.get_red_ghost_spawn_position()
        Character.__init__(self, level, image, scale_factor, arena_position, direction)

    def __bfs(self, starting_point, target):
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

    def follow(self, target):
        self.target = target

    def update(self):
        if self.target is not None:
            shortest_path_to_target = self.__bfs(self.arena_position, self.target.arena_position)

            if shortest_path_to_target is not None and len(shortest_path_to_target) >= 2:
                self.arena_position = self.__bfs(self.arena_position, self.target.arena_position)[1]
                self.rect = self.image.get_rect().move(self.level.get_position_from_arena_position(self.arena_position))
