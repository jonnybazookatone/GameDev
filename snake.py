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

    def __init__(self, x=0, y=0, width=50, height=50, colour=(0, 0, 0), vx=0, vy=0, bounds=[0, 0], edge_behaviour=-1, chain_number=0):
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

        # Snake properties
        self.chain_number = chain_number
        self.position_list = []

        self.infront = None
        self.wait = 0

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

    def add_move(self, dx, dy, wait):
    	self.position_list.append([dx, dy, wait])

    def remove_move(self):
	self.position_list = self.position_list[1:]

    def deduct_move(self):
	for i in range(len(self.position_list)):
		self.position_list[i][2] = self.position_list[i][2] - 1

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

    def set_infront(self, infront):
    	self.infront = infront

    def get_infront(self):
    	return self.infront
    def set_wait(self, wait):
    	self.wait = wait
    def get_wait(self):
    	return self.wait

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

width = 20
snake1 = MovingBoxSprite(x=60-1*width, y=0, width=width, height=20, colour=BLACK, vx=1, vy=0, bounds=size, chain_number=0)
snake2 = MovingBoxSprite(x=60-2*width, y=0, width=width, height=20, colour=BLACK, vx=1, vy=0, bounds=size, chain_number=1)

snake2.set_infront(snake1)

snake_chain.add(snake1)
snake_chain.add(snake2)

font = pygame.font.Font(None, 50)

x_coord2, y_coord2 = 1, 0

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
    # User pressed down on a key
    if event.type == pygame.KEYDOWN:
    # Figure out if it was an arrow key. If so
    # adjust speed.
        if event.key == pygame.K_UP:
            y_coord2 = -1
            x_coord2 = 0
        if event.key == pygame.K_DOWN:
            y_coord2 = 1
            x_coord2 = 0
        if event.key == pygame.K_LEFT:
        	y_coord2 = 0
        	x_coord2 = -1
        if event.key == pygame.K_RIGHT:
        	y_coord2 = 0
        	x_coord2 = 1
    # User let up on a key
    #if event.type == pygame.KEYUP:
        # If it is an arrow key, reset vector back to zero
    #    if event.key == pygame.K_UP:
    #        y_coord2 = 0
    #    if event.key == pygame.K_DOWN:
    #        y_coord2 = 0
    #    if event.key == pygame.K_LEFT:
    #    	x_coord2 = 0
    #    if event.key == pygame.K_RIGHT:
    #    	x_coord2 = 0
    
    # Random title for now
    text = font.render("Snake the Game", True, BLACK)
    screen.blit(text, [size[0]/2, 0])   # Put the image of the text on the screen

    curr_vx, curr_vy = snake1.get_velocity()
    if (y_coord2 != 0 and curr_vy == 0) or (x_coord2 != 0 and curr_vx == 0):
		snake1.set_velocity(x_coord2, y_coord2)
		snake1.set_wait(1)
    else:
		snake1.set_wait(0)

    snake1.move()

    for chain in snake_chain:
    	if chain.get_infront():
            infront = chain.get_infront()
            vx, vy = infront.get_velocity()
            wait = infront.get_wait()
            chain.add_move(vx, vy, wait*chain.get_width()*chain.chain_number)

    for chain in snake_chain:
        if chain.get_infront():
            
            print chain.position_list

    	    if chain.position_list[0][2] == 0:
    	    	chain.set_velocity(chain.position_list[0][0], chain.position_list[0][1])
    	    	chain.remove_move()
    	    else:
    	    	chain.deduct_move()

    		chain.move()

    # Draw to the screen
    snake_chain.draw(screen)
    
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(1)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
