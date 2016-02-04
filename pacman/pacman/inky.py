from .ghost import Ghost
from .character import Character


class Inky(Ghost):
    name = "Inky"

    def __init__(self, level, image, scale_factor, direction):
        arena_position = level.get_inky_spawn_position()
        Character.__init__(self, level, image, scale_factor, arena_position, direction)
