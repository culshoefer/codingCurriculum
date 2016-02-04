from .ghost import Ghost
from .character import Character


class Pinky(Ghost):
    name = "Pinky"

    def __init__(self, level, image, scale_factor, direction, speed):
        arena_position = level.get_pinky_spawn_position()
        Character.__init__(self, level, image, scale_factor, arena_position, direction, speed)
