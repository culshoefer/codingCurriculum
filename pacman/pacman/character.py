import pygame

NUM_DIRECTIONS = 4
ROTATION_ANGLE = (360/NUM_DIRECTIONS)


class Character(pygame.sprite.Sprite):
    image = None
    rect = None
    next_direction = None  # right = 0, up = 1, left = 2, down = 3
    curr_direction = None
    arena_position = None  # (row, col)

    def __init__(self, level, image, scale_factor, arena_position, direction):
        pygame.sprite.Sprite.__init__(self)

        self.level = level

        self.image = pygame.image.load(image)
        image_width, image_height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(image_width * scale_factor), int(image_height * scale_factor)))
        self.image = pygame.transform.rotate(self.image, direction * ROTATION_ANGLE)
        self.curr_direction = direction

        self.arena_position = arena_position
        self.rect = self.image.get_rect().move(level.get_position_from_arena_position(arena_position))

    def set_direction(self, direction):
        assert direction in range(NUM_DIRECTIONS), "pacman.character: tried to set invalid direction {}.\n".format(direction)

        self.next_direction = direction

    def update_direction(self):
        if self.next_direction is not None and self.level.is_accessible(self.get_next_cell_in_direction(self.next_direction)):
            self.image = pygame.transform.rotate(self.image, (self.next_direction - self.curr_direction) * ROTATION_ANGLE)

            self.curr_direction = self.next_direction
            self.next_direction = None

    def get_next_cell_in_direction(self, direction):
        return self.level.get_next_cell_in_direction(self.arena_position, direction)

    def update(self):
        self.update_direction()
        next_cell = self.get_next_cell_in_direction(self.curr_direction)

        if self.level.is_accessible(next_cell):
            self.arena_position = next_cell
            self.rect = self.image.get_rect().move(self.level.get_position_from_arena_position(self.arena_position))
