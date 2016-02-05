import pygame
from .character import Character, NUM_DIRECTIONS
import random

NUM_MODES = 3
CHASE_MODE = 0
SCATTER_MODE = 1
FRIGHTENED_MODE = 2

FRIGHTENED_DURATION = 5000  # ms

class Ghost(Character):
    normal_image = None
    frightened_image = None

    target = None
    mode = None
    frightened_at_time = None

    def __init__(self, level, normal_image, frightened_image, scale_factor, arena_position, direction, speed):
        self.mode = CHASE_MODE
        self.time_frightened = 0

        self.normal_image = pygame.image.load(normal_image)
        image_width, image_height = self.normal_image.get_size()
        self.normal_image = pygame.transform.scale(self.normal_image, (int(image_width * scale_factor), int(image_height * scale_factor)))

        self.frightened_image = pygame.image.load(frightened_image)
        image_width, image_height = self.frightened_image.get_size()
        self.frightened_image = pygame.transform.scale(self.frightened_image, (int(image_width * scale_factor), int(image_height * scale_factor)))


        Character.__init__(self, level, normal_image, scale_factor, arena_position, direction, speed)

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

    def frighten(self):
        self.mode = FRIGHTENED_MODE
        self.frightened_at_time = pygame.time.get_ticks()
        self.speed *= 0.25
        self.image = self.frightened_image

    def _unfrighten(self):
        self.mode = CHASE_MODE
        self.frightened_at_time = None
        self.speed *= 4
        self.image = self.normal_image

    def _frightened(self):
        self.curr_direction = random.randint(0, NUM_DIRECTIONS - 1)

    def _chase(self):
        self.curr_direction = self._direction_to(self.target.arena_position)

    def set_target(self, target):
        self.target = target

    def handle_collision(self):
        if self.mode == FRIGHTENED_MODE:
            print "You ate {}".format(self.name)
            self.respawn()
            return False
        else:
            print "You were eaten by {}.".format(self.name)
            return True


    def update(self):
        if self.mode == FRIGHTENED_MODE and (pygame.time.get_ticks() - self.frightened_at_time) > FRIGHTENED_DURATION:
            self._unfrighten()

        if self.level.is_turning_point(self.arena_position):
            if self.mode == CHASE_MODE:
                self._chase()
            elif self.mode == FRIGHTENED_MODE:
                self._frightened()

        next_cell = self.get_next_cell_in_direction(self.curr_direction)
        if self.level.is_accessible(next_cell):
            self.arena_position = next_cell
            self.rect = self.image.get_rect().move(self.level.get_position_from_arena_position(self.arena_position))
