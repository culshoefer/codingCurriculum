from future import division

import random

import pygame


class Mole(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("mole.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = False

    def __str__(self):
        return "pos: ({}, {}) groups: {}".format(self.rect.x,
                                                 self.rect.y, str(self.groups))

    def show(self, visible):
        self.visible = visible


def check_win():
    # if all moles are hidden (not visible)
    if all(not mole.visible for row in board for mole in row):
        # remove them from all sprites JUST to be sure
        for row in board:
            for mole in row:
                all_sprites.remove(mole)

        screen.blit(
            pygame.font.Font(None, 45).render("You won!", 1, (0, 0, 0)),
            (250, 250)
        )

# set-up for the application
pygame.init()
screen = pygame.display.set_mode((568 + 50, 568 + 50))

all_sprites = pygame.sprite.Group()

board = [[None for i in range(4)] for j in range(4)]
for i in range(0, 608, 152):
    for j in range(0, 608, 152):
        temp = Mole(i + 10, j + 10)

        if random.random() < 0.5:
            temp.show(True)
            all_sprites.add(temp)

        board[i // 152][j // 152] = temp

last_position = (-1, -1)
while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        # if we clicked X button
        if event.type == pygame.QUIT:
            pygame.quit()
        # if we clicked a mouse button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get the position of the click and corresponding tile
            last_position = x, y = pygame.mouse.get_pos()
            current_tile = board[x // 152][y // 152]

            if current_tile.visible:
                all_sprites.remove(current_tile)
                current_tile.show(False)
            else:  # skip the current iteration
                continue

            check_win()

            # map the (x, y) into array indices
            x, y = map(lambda x: x // 152, last_position)
            # BFS around current tile
            for dx, dy in zip([0, 0, 1, -1], [-1, 1, 0, 0]):
                # if the tile we try to modify is inside the board
                if 0 <= x + dx <= 3 and 0 <= y + dy <= 3:
                    current_tile = board[x + dx][y + dy]
                    if current_tile.visible:
                        all_sprites.remove(current_tile)
                        current_tile.show(False)
                    else:
                        all_sprites.add(current_tile)
                        current_tile.show(True)

    check_win()

    all_sprites.draw(screen)
    pygame.display.flip()
