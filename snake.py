"""
 Snake game based on those found on mobile phones.

  Uses pygame libraries and material from the guide given by  http://programarcadegames.com/

  Snake is controlled by the LEFT, RIGHT, UP and DOWN arrow keys.

  Scoring will continue forever.
"""

import pygame
import random

# Lets work on sprites instead of the hack I have used
class MovingBoxSprite(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, width=50, height=50, colour=(0, 0, 0), vx=0, vy=0, bounds=[0, 0], edge_behaviour=-1):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self._Name = ""
        self._width = width
        self._height = height
        self._colour = colour
        self._edge_behaviour = edge_behaviour
        self._vx = vx
        self._vy = vy
        self._bounds = bounds

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([self._width, self._height])
        self.image.fill(self._colour)
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        self._x = x
        self._y = y

        self.rect.x = x
        self.rect.y = y

        # Below is a class that mimics the behaviour of a sprite, but is most likely overkill and less efficient than the
        # ones inbuilt in pygame

    def change_position(self, dx, dy):

        if self.rect.x+dx+self._width >= self._bounds[0]:
            dx *= self._edge_behaviour
        elif self.rect.x+dx <= 0:
            dx = abs(dx*self._edge_behaviour)

        if self.rect.y+dy+self._height >= self._bounds[1]:
            dy *= self._edge_behaviour
        elif self.rect.y+dy <= 0:
            dy = abs(dy*self._edge_behaviour)

        self.rect.x += dx
        self.rect.y += dy

        return dx, dy

    def move(self):
        if abs(self._vx) > 0 or abs(self._vy) > 0:
            self._vx, self._vy = self.change_position(self._vx, self._vy)

    def set_velocity(self, vx, vy):
        self._vx = vx
        self._vy = vy

    def get_velocity(self):
        return self._vx, self._vy

    def reset_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_width(self):
        return self._width

# Define some colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (227, 14, 14)

pygame.init()

# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Snake the Game")
# click_sound = pygame.mixer.Sound("pong/click.wav")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

snake_chain = pygame.sprite.Group()
snake = MovingBoxSprite(x=60, y=0, width=20, height=20, colour=BLACK, vx=10, vy=10, bounds=size)
snake_chain.add(snake)

font = pygame.font.Font(None, 50)

x_coord2, y_coord2 = 0, 0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # If user clicked close
            done = True     # Flag that we are done so we exit this loop

    # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)

    # KEYBOARD INPUT
    # PLAYER
    ################
    x_coord2, y_coord2 = 0, 0
    # User pressed down on a key
    if event.type == pygame.KEYDOWN:
    # Figure out if it was an arrow key. If so
    # adjust speed.
        if event.key == pygame.K_UP:
            y_coord2 = -10
        if event.key == pygame.K_DOWN:
            y_coord2 = 10
        if event.key == pygame.K_LEFT:
        	x_coord2 = -10
        if event.key == pygame.K_RIGHT:
        	x_coord2 = 10
    # User let up on a key
    if event.type == pygame.KEYUP:
        # If it is an arrow key, reset vector back to zero
        if event.key == pygame.K_UP:
            y_coord2 = 0
        if event.key == pygame.K_DOWN:
            y_coord2 = 0
        if event.key == pygame.K_LEFT:
        	x_coord2 = 0
        if event.key == pygame.K_RIGHT:
        	x_coord2 = 0
    
    # Random title for now
    text = font.render("Snake the Game", True, BLACK)
    screen.blit(text, [size[0]/2, 0])   # Put the image of the text on the screen

    snake.set_velocity(x_coord2, y_coord2)


    for chain in snake_chain:
    	chain.move()

    # Draw to the screen
    snake_chain.draw(screen)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()