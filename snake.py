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
        self.number_of_chains = 0

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
        # for i in range(len(self.position_list)):
            self.position_list[0][2] = self.position_list[0][2] - 1

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

    def set_move(self):
        self.set_velocity(self.position_list[0][0], self.position_list[0][1])


# Define some colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (227, 14, 14)
GREY = (100, 100, 100)
BLUE = (0, 0, 255)

pygame.init()

# Set the width and height of the screen [width, height]
size = (500, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Snake the Game")
# click_sound = pygame.mixer.Sound("pong/click.wav")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

snake = pygame.sprite.Group()
snake_chain = pygame.sprite.Group()
eatme_list = pygame.sprite.Group()
eat_me = False

width = 20
start_vx = 1
snake1 = MovingBoxSprite(x=60-1*width, y=0, width=width, height=20, colour=BLUE, vx=start_vx, vy=0, bounds=size,
                         chain_number=0)
# snake2 = MovingBoxSprite(x=60-2*width, y=0, width=width, height=20, colour=BLUE, vx=start_vx, vy=0, bounds=size,
#                          chain_number=1)
# snake3 = MovingBoxSprite(x=60-3*width, y=0, width=width, height=20, colour=BLUE, vx=start_vx, vy=0, bounds=size,
#                          chain_number=2)
# snake4 = MovingBoxSprite(x=60-4*width, y=0, width=width, height=20, colour=BLUE, vx=start_vx, vy=0, bounds=size,
#                          chain_number=3)
snake1.set_wait(100)
# snake2.set_infront(snake1)
# snake3.set_infront(snake2)
# snake4.set_infront(snake3)

snake.add(snake1)
# snake_chain.add(snake2)
# snake_chain.add(snake3)
# snake_chain.add(snake4)

font = pygame.font.Font(None, 30)
score = 0
x_coord2, y_coord2 = 1, 0
yes = True


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
            y_coord2 = -1 * start_vx
            x_coord2 = 0
        if event.key == pygame.K_DOWN:
            y_coord2 = start_vx
            x_coord2 = 0
        if event.key == pygame.K_LEFT:
            y_coord2 = 0
            x_coord2 = -1 * start_vx
        if event.key == pygame.K_RIGHT:
            y_coord2 = 0
            x_coord2 = start_vx

    # Random title for now
    time = int(pygame.time.get_ticks())  # miliseconds
    time /= 1000

    score_text = font.render("Score: %d" % score, True, BLACK)
    time_text = font.render("Time: %d seconds" % int(time), True, BLACK)
    screen.blit(score_text, [500, 0])   # Put the image of the text on the screen
    screen.blit(time_text, [500, 20])

    curr_vx, curr_vy = snake1.get_velocity()
    if ( (y_coord2 != 0 and curr_vx != 0) or (x_coord2 != 0 and curr_vy != 0) ) and snake1.get_wait():

        snake1.set_velocity(x_coord2, y_coord2)

        for chain in snake_chain:
            vx, vy = snake1.get_velocity()

            # Go further than the snake width?
            steps = snake1.get_wait()
            if steps < chain.get_width():
                chain.add_move(vx, vy, (steps-1)*(chain.chain_number-1))
            else:
                chain.add_move(vx, vy, (snake1.get_width()*(chain.chain_number)))

            # print("Chain #: %d" % chain.chain_number)
            # print("Wait: %f" % wait)
            # print("Length: %f" % (snake1.get_width()*chain.chain_number))
            # if wait < snake1.get_width() * chain.chain_number:
            #     wait = snake1.get_width() * chain.chain_number
            # else:
            #     wait = snake1.get_width()* chain.chain_number


        print(snake1.get_wait())
        snake1.set_wait(0)

    snake1.move()
    snake1.set_wait(snake1.get_wait()+1)
    # print("Snake wait: %f" % snake1.get_wait())

    for chain in snake_chain:

        if chain.position_list:
            print(chain.chain_number, chain.position_list)
            if chain.position_list[0][2] == 0:
                chain.set_move()
                chain.remove_move()
                # print(chain.chain_number, chain.position_list)

                # print(chain.position_list[0][2])
            else:
                chain.deduct_move()

        chain.move()

    if not eat_me:
        X = random.random()*size[0]
        Y = random.random()*size[1]

        eat_me = MovingBoxSprite(x=X, y=Y, width=width, height=20, colour=RED, vx=0, vy=0, bounds=size)

        eatme_list.add(eat_me)

    did_i_eat_list = pygame.sprite.spritecollide(snake1, eatme_list, True)

    if did_i_eat_list:
        eat_me = False

        # Make extra chain

	tmp = snake1
	for sn in snake_chain:
		if sn.chain_number > tmp.chain_number:
			tmp = sn

        X_new = tmp.rect.x
        Y_new = tmp.rect.y
        VX, VY = tmp.get_velocity()

        NUM = snake1.number_of_chains
        snake1.number_of_chains = NUM + 1

	# moving to the right
        if VX > 0: 
            X_new -= width
	# moving to the left
	elif VX < 0:
	    X_new += width
	# moving down
        elif VY > 0:
            Y_new -= width
	# moving up
	elif VY < 0:
	    Y_new += width
        
	new_snake = MovingBoxSprite(x=X_new, y=Y_new, width=width, height=20, colour=BLUE, vx=VX, vy=VY,
                                 bounds=size, chain_number=NUM+1)
	#new_snake.add_move(VX, VY, 0)
	#for i in tmp.position_list:
	#	print i
	#	new_snake.position_list.append(i)
        snake_chain.add(new_snake)
        print(new_snake.get_velocity())
        #new_snake.move()
        yes = False
        score += 1

    # Draw to the screen
    snake.draw(screen)
    snake_chain.draw(screen)
    eatme_list.draw(screen)




    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
