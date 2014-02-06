"""
 Pong game.

 Uses pygame libraries and followed a guide given by  http://programarcadegames.com/

 Left bat is controlled by a joystick.
 Right bat is controlled by the UP and DOWN arrow keys.

 Scoring will continue forever.

"""

import pygame
import random
import sys


class MovingBox(object):

    def __init__(self):
        self._Name = ""
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self._color = (0, 0, 0)
        self._edge_behaviour = -1
        self._vx = 0
        self._vy = 0
        self._bounds = [0, 0]

    def set_attributes(self, x, y, width, height, colour, edge_behaviour, bounds, vx=0, vy=0):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._colour = colour
        self._edge_behaviour = edge_behaviour
        self._vx = vx
        self._vy = vy
        self._bounds = bounds

    def reset_position(self, x, y):
        self._x = x
        self._y = y

    def change_position(self, dx, dy):

        if self._x+dx+self._width >= self._bounds[0]:
            dx *= self._edge_behaviour
        elif self._x+dx <= 0:
            dx = abs(dx*self._edge_behaviour)

        if self._y+dy+self._height >= self._bounds[1]:
            dy *= self._edge_behaviour
        elif self._y+dy <= 0:
            dy = abs(dy*self._edge_behaviour)

        self._x += dx
        self._y += dy

        return dx, dy

    def draw(self, screen):

        if abs(self._vx) > 0 or abs(self._vy) > 0:
            self._vx, self._vy = self.change_position(self._vx, self._vy)

        pygame.draw.rect(screen, self._colour, [self._x, self._y, self._width, self._height], 0)

# Define some colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pong")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

bat1 = MovingBox()
bat1.set_attributes(x=10, y=size[1]/2, width=30, height=100, colour=WHITE, edge_behaviour=0, bounds=size)

bat2 = MovingBox()
bat2.set_attributes(x=660, y=size[1]/2, width=30, height=100, colour=WHITE, edge_behaviour=0, bounds=size)

ball = MovingBox()
ball.set_attributes(x=100, y=140, width=50, height=50, colour=WHITE, edge_behaviour=-1, bounds=size, vx=10, vy=10)

font = pygame.font.Font(None, 50)

left_score, right_score = 0, 0
x_coord1, x_coord2, y_coord1, y_coord2 = 0, 0, 0, 0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop

    # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    # Count the joysticks the computer has
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        # No joysticks!
        print("Error, I didn't find any joysticks.")
    else:
        # Use joystick #0 and initialize it
        my_joystick = pygame.joystick.Joystick(0)
        my_joystick.init()

    # As long as there is a joystick
    if joystick_count != 0:
        # This gets the position of the axis on the game controller
        # It returns a number between -1.0 and +1.0
        horiz_axis_pos = my_joystick.get_axis(0)
        vert_axis_pos = my_joystick.get_axis(1)
        # Move x according to the axis. We multiply by 10 to speed up the movement.
        x_coord1 = int(horiz_axis_pos * 10)
        y_coord1 = int(vert_axis_pos * 10)

    x_coord2, y_coord2 = 0, 0
    # User pressed down on a key
    if event.type == pygame.KEYDOWN:
    # Figure out if it was an arrow key. If so
    # adjust speed.
        if event.key == pygame.K_UP:
            y_coord2 = -10
        if event.key == pygame.K_DOWN:
            y_coord2 = 10
    # User let up on a key
    if event.type == pygame.KEYUP:
        # If it is an arrow key, reset vector back to zero
        if event.key == pygame.K_UP:
            y_coord2 = 0
        if event.key == pygame.K_DOWN:
            y_coord2 = 0


    if ball._x == bat1._x + bat1._width and ball._y+ball._height >= bat1._y and ball._y <= bat1._y + bat1._height:
        ball._vx *= -1
        # ball._vy *= -1


    if ball._x + ball._width == bat2._x and ball._y+ball._height >= bat2._y and ball._y <= bat2._y + bat2._height:
        ball._vx *= -1
        # ball._vy *= -1

    line = pygame.draw.rect(screen, WHITE, [size[0]/2, 0, 2, size[1]], 0)

    if ball._x < bat1._width:
        right_score += 1
        ball.reset_position(x=600, y=50)
        ball._vx = -1*abs(ball._vx)
        ball._vy = -1*abs(ball._vy)
        ball.draw(screen)

    elif ball._x + ball._width > bat2._x:
        left_score += 1
        ball.reset_position(x=50, y=50)
        ball._vx = abs(ball._vx)
        ball._vy = abs(ball._vy)
        ball.draw(screen)

    else:
        bat1.change_position(dx=x_coord1, dy=y_coord1)
        bat1.draw(screen)

        bat2.change_position(dx=x_coord2, dy=y_coord2)
        bat2.draw(screen)

        ball.draw(screen)



    text_left = font.render("%d" % left_score, True, WHITE)
    text_right = font.render("%d" % right_score, True, WHITE)
    text_dx = 100
    screen.blit(text_left, [size[0]/2 - text_dx, 0])   # Put the image of the text on the screen
    screen.blit(text_right, [size[0]/2 + text_dx, 0])   # Put the image of the text on the screen

    before = now


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(30)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()