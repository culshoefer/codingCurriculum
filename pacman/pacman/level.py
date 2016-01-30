import pygame

# Values to encode information in internal logic
EMPTY_BLOCK = 0
WALL_BLOCK = 1
GHOST_ONLY_BLOCK = 2

BLINKY_SPAWN_BLOCK = 3
PINKY_SPAWN_BLOCK = 4
INKY_SPAWN_BLOCK = 5
CLYDE_SPAWN_BLOCK = 6

PACMAN_SPAWN_BLOCK = 7

# Colors used to encode the information in the level descriptor image
EMPTY_BLOCK_COLOR = (255, 255, 255)
WALL_BLOCK_COLOR = (0, 0, 0) 
GHOST_ONLY_BLOCK_COLOR = (136, 136, 136)

BLINKY_SPAWN_BLOCK_COLOR = (221, 0, 0)
PINKY_SPAWN_BLOCK_COLOR = (255, 153, 153)
INKY_SPAWN_BLOCK_COLOR = (102, 255, 255)
CLYDE_SPAWN_BLOCK_COLOR = (255, 153, 0)

PACMAN_SPAWN_BLOCK_COLOR = (255, 255, 51)

spawn_blocks = [BLINKY_SPAWN_BLOCK, PINKY_SPAWN_BLOCK, INKY_SPAWN_BLOCK, CLYDE_SPAWN_BLOCK, PACMAN_SPAWN_BLOCK]

# Dictionaries from blocks to colors and viceversa
block_to_color_mapping = {EMPTY_BLOCK:EMPTY_BLOCK_COLOR, WALL_BLOCK:WALL_BLOCK_COLOR, GHOST_ONLY_BLOCK:GHOST_ONLY_BLOCK_COLOR,
        BLINKY_SPAWN_BLOCK:BLINKY_SPAWN_BLOCK_COLOR, PINKY_SPAWN_BLOCK:PINKY_SPAWN_BLOCK_COLOR,
        INKY_SPAWN_BLOCK:INKY_SPAWN_BLOCK_COLOR, CLYDE_SPAWN_BLOCK:CLYDE_SPAWN_BLOCK_COLOR,
        PACMAN_SPAWN_BLOCK:PACMAN_SPAWN_BLOCK_COLOR}

color_to_block_mapping = {v:k for k, v in block_to_color_mapping.items()}


class Level():
    # Matrix that holds the level details
    arena = []
    arena_width = None
    arena_height = None
    screen_size = None

    def __init__(self, screen_size, level_file):
        self.screen_size = screen_size

        level_image = pygame.image.load(level_file)
        px_array = pygame.PixelArray(level_image)

        width = len(px_array[0])
        height = len(px_array)

        # PixelArrays are addressed [column][row]
        # arena is addressed [row][column]
        # That's why things are flipped
        self.arena_width = height
        self.arena_height = width

        # Read and decode level descriptor
        for row in range(self.arena_height):
            self.arena.append([])
            for col in range(self.arena_width):
                try:
                    # Have to do this "unboxing" because pygame.Color is not hashable, so it cannot be put in a dictionary
                    current_color = level_image.unmap_rgb(px_array[col][row])
                    color_tuple = (current_color.r, current_color.g, current_color.b)

                    self.arena[row].append(color_to_block_mapping[color_tuple])

                except KeyError:
                    raise ValueError("{0} is not a valid level descriptor image: encountered color {1}\n".format(level_file, px_array[row][col]))

    def get_position_from_arena_position(self, arena_position):
        width, height = self.screen_size
        arena_row, arena_col = arena_position

        aspect_ratio = width/self.arena_width 

        return (aspect_ratio*arena_col, aspect_ratio * arena_row)

    def is_accessible(self, arena_position):
        arena_row, arena_col = arena_position
        is_wall = True if (self.arena[arena_row][arena_col] == WALL_BLOCK) else False

        return (not is_wall)

    def get_surface(self):

        width, height = self.screen_size
        surface = pygame.Surface((width, height))
        px_array = pygame.PixelArray(surface)


        # Sprite and arena must have same aspect ratio

        assert ((width % self.arena_width == 0) and (height % self.arena_height == 0) and
                (width/self.arena_width == height/self.arena_height)), "Requested sprite size is incompatible with arena size.\n"

        aspect_ratio = width/self.arena_width


        # For each block in the arena
        for row in range(self.arena_height):
            for col in range(self.arena_width):
                color = block_to_color_mapping[self.arena[row][col]]

                # Don't draw spawn points and ghost only blocks
                if (self.arena[row][col] in spawn_blocks) or self.arena[row][col] == GHOST_ONLY_BLOCK:
                    color = (255, 255, 255)

                # Draw the pixels
                for p_row in range(aspect_ratio):
                    for p_col in range(aspect_ratio):
                        px_array[aspect_ratio*col + p_col][aspect_ratio*row + p_row] = color 


        return px_array.make_surface()


