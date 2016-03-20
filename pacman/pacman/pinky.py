from .ghost import Ghost


class Pinky(Ghost):
    name = "Pinky"

    def __init__(self, level, image, frightened_image, scale_factor, direction, speed):
        arena_position = level.get_pinky_spawn_position()
        Ghost.__init__(self, level, image, frightened_image, scale_factor, arena_position, direction, speed)

    def respawn(self):
        self._unfrighten()
        self.arena_position = self.level.get_pinky_spawn_position()
