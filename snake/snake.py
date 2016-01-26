import pygame

pygame.init()
#######################################################
#######################################################
##                                                   ##
##                do NOT change anything here        ##
##                                                   ##
#######################################################
#######################################################

# class snake
# position: arr holding the coordinates of the head of the snake
# body : 2D arr holding position of body parts ~ to the head 
# direction : arr holding the direction [x, y] 

class Position:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
    def X(self):
        return self.x
    def Y(self):
        return self.y
    def changePosition(change_x, change_y):
        self.x = change_x
        self.y = change_y


class snake:
    def __init__(self, x_pos, y_pos):
        self.direction = [1, 0]
        self.position = Position(x_pos, y_pos)
        
    def changeDirection(change_x, change_y):
        self.direction = [change_x, change_y]
    def moveForward(self):
        self.position.setPosition(self.direction[0], self.direction[1])





# game constants
screen_width = 320
screen_height= 240
field_columns = screen_width / 10
field_rows = screen_height / 10

gamefield = [[0 for x in range(field_columns)] for x in range(field_rows)]

# colours
BLACK = (0x00, 0x00, 0x00)



# SETUP

#setup the screen
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snake")



done = False
clock = pygame.time.Clock()

# game loop
while not done:
    # Keyboard Input and events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                print("KEYDOWN")
            elif event.key == pygame.K_UP:
                print("KEYUP")
            elif event.key == pygame.K_LEFT:
                print("KEYLEFT")
            elif event.key == pygame.K_RIGHT:
                print("KEYRIGHT")

    #Game logic should go here

    # Drawing code should go here
    screen.fill(BLACK)

    pygame.display.flip()

    clock.tick(60)


