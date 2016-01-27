import pygame

pygame.init()
#######################################################
#######################################################
##                                                   ##
##                do NOT change anything here        ##
##                                                   ##
#######################################################
#######################################################


# gamefield:
# x|y
# 0|0 1|0 2|0 3|0 4|0 5|0 6|0 7|0 .. width|0
# 0|1 1|1 2|1 3|1 4|1 5|1 6|1 7|1       :
# 0|2 1|2 2|2 3|2 4|2 5|2 6|2 7|2       :
# 0|3 1|3 2|3 3|3 4|3 5|3 6|3 7|3       :
#  :                              .     :
#  :                                .   :
# 0|height ..........................width|height


# class position, makes it easier to understand the code 
# of the class Snake
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
    def __repr__(self):
        return str(self.X()) + "|" + str(self.Y()) + " "
    def __str__(self):
        return str(self.X()) + "|" + str(self.Y()) + " "

class Direction:
    def __init__(self, x_direction, y_direction):
        self.x = x_direction
        self.y = y_direction
    def X(self):
        return self.x
    def Y(self):
        return self.y
    def rotateClockwise():
        tmp_x = self.x
        self.x = self.y
        self.y = -1 * tmp_x
    def rotateAnticlockwise():
        tmp_x = self.x
        self.x = -1 * self.y
        self.y = tmp_x
    def __eq__(self, direction):
        return self.x == direction.X() and self.y == direction.Y() 

class SnakeBody:
    def __init__(self, headposition, num_of_bodyparts):
        self.arr = []
        for i in range(1, num_of_bodyparts+1):
            self.arr.append(Position( headposition.X()-i, headposition.Y() ))
    def getNumOfBodyparts(self):
        return len(arr)
    def addBodypart(self, position):
        self.arr.append(position)
    def getBodypart(self, number):
        if number < len(arr) and number >= 0:
            px = self.arr[number]
            py = self.arr[number]
            return Position(px, py)
    def __repr__(self):
        s = ""
        for i in range(0, len(self.arr)):
            s += str(self.arr[i])
        return s
    def __str__(self):
        s = ""
        for i in range(0, len(self.arr)):
            s += str(self.arr[i])
        return s


# class snake
# body : 2D arr holding position of body parts ~ to the head 
# direction : arr holding the direction [x, y] 
class Snake:
    def __init__(self, x_pos, y_pos, body=4):
        self.direction = Direction(1, 0)
        self.position = Position(x_pos, y_pos)
        self.body = SnakeBody(self.position, body);
    def changeDirection(change_x, change_y):
        self.direction = [change_x, change_y]
    def moveForward(self):
        self.position.changePosition(self.direction[0], self.direction[1])
    def moveRight(self):
        self.direction.rotateClockwise
    def moveLeft(self):
        self.direction.rotateAnticlockwise
    def __repr__(self):
        return "Head: " + str(self.position) + " Body: " + str(self.body) 
    def __str__(self):
        return "Head: " + str(self.position) + " Body: " + str(self.body) 




# game constants
square_size = 10
screen_width = 320
screen_height= 240
field_columns = screen_width / square_size
field_rows = screen_height / square_size

LEFT = Direction(-1, 0)
RIGHT = Direction(1, 0)
DOWN = Direction(0, 1)
UP = Direction(0, -1)

gamefield = [[0 for x in range(field_columns)] for x in range(field_rows)]

# colours
BLACK = (0x00, 0x00, 0x00)





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
    snake = Snake(int(field_columns/2), int(field_rows/2))
    print snake


    # Drawing code should go here
    screen.fill(BLACK)

    pygame.display.flip()

    clock.tick(60)


