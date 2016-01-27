import pygame


class Mole(pygame.sprite.DirtySprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("mole.jpg").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.visible = True

    def __str__(self):
        return "pos: ({}, {}) groups: {}".format(self.rect.x,
                                                 self.rect.y, str(self.groups))

# set-up for the application
pygame.init()
screen = pygame.display.set_mode((568 + 50, 568 + 50))

all_sprites = pygame.sprite.Group()

board = [[None for i in range(4)] for j in range(4)]
for i in range(0, 608, 152):
    for j in range(0, 608, 152):
        temp = Mole(i + 10, j + 10)
        board[i // 152][j // 152] = temp
        all_sprites.add(temp)

for row in board:
    for mole in row:
        mole.groups = all_sprites

last_position = (-1, -1)
while True:
    if last_position != (-1, -1):
        x, y = map(lambda x: x // 152, last_position)
        for dx, dy in zip([0, 0, 1, -1], [-1, 1, 0, 0]):
            if 0 <= x + dx <= 3 and 0 <= y + dy <= 3:
                all_sprites.add(board[x + dx][y + dy])

    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.MOUSEBUTTONDOWN:
            last_position = x, y = pygame.mouse.get_pos()
            all_sprites.remove(board[x // 152][y // 152])
            print(last_position)

    all_sprites.draw(screen)
    pygame.display.flip()
    # pygame.display.update()
