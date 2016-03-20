import pygame


class Dot(pygame.sprite.Sprite):
    image = None
    rect = None
    level = None
    arena_position = None
    is_super = None

    def __init__(self, level, image, arena_position, is_super=False):
        pygame.sprite.Sprite.__init__(self)

        self.is_super = is_super

        self.level = level

        self.image = pygame.image.load(image)
        self.arena_position = arena_position
        
        self.rect = self.image.get_rect().move(level.get_position_from_arena_position(arena_position))

