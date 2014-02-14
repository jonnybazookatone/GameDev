"""
 Snake game based on those found on mobile phones.

  Uses pygame libraries and material from the guide given by  http://programarcadegames.com/

  Snake is controlled by the LEFT, RIGHT, UP and DOWN arrow keys.

  Scoring will continue forever.
"""

import pygame
import random
import sys


# Lets work on sprites instead of the hack I have used
class MovingBoxSprite(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, width=50, height=50, colour=(0, 0, 0), vx=0, vy=0, bounds=(0, 0), edge_behaviour=1, chain_number=0):
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
        self.number_of_chains = 0
        self.hit = False

    def change_position(self, dx, dy):

        hit = False

        if self.rect.x+dx+self._width >= self._bounds[0]:
            dx *= self._edge_behaviour
            hit = True
        elif self.rect.x+dx <= 0:
            dx = abs(dx*self._edge_behaviour)
            hit = True

        if self.rect.y+dy+self._height >= self._bounds[1]:
            dy *= self._edge_behaviour
            hit = True
        elif self.rect.y+dy <= 0:
            dy = abs(dy*self._edge_behaviour)
            hit = True

        self.rect.x += dx
        self.rect.y += dy

        return dx, dy, hit

    def move(self):

        if abs(self._vx) > 0 or abs(self._vy) > 0:
            self._vx, self._vy, self.hit = self.change_position(self._vx, self._vy)

    def get_hit(self):
        return self.hit

    def set_velocity(self, vx, vy):
        self._vx = vx
        self._vy = vy

    def get_velocity(self):
        return self._vx, self._vy

# Define some colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (227, 14, 14)
GREY = (100, 100, 100)
BLUE = (0, 0, 255)


def game_setup(width, start_vx):

    # Define the initial snake
    snake1 = MovingBoxSprite(x=60, y=10, width=width, height=width, colour=BLUE, vx=start_vx, vy=0, bounds=size,
                             chain_number=0)
    snake2 = MovingBoxSprite(x=60-1*width, y=10, width=width, height=width, colour=BLUE, vx=start_vx, vy=0, bounds=size,
                             chain_number=1)
    snake3 = MovingBoxSprite(x=60-2*width, y=10, width=width, height=width, colour=BLUE, vx=start_vx, vy=0, bounds=size,
                             chain_number=2)
    # This refers to the other parts of the snake that are not the head
    snake1.number_of_chains = 2

    snake = pygame.sprite.Group()
    snake.add(snake1)
    snake.add(snake2)
    snake.add(snake3)

    # Add the sprites to a Sprite group and create the eatable blob Sprite group
    eat_me_list = pygame.sprite.Group()
    eat_me = False

    pos_list = [[start_vx, 0], [start_vx, 0]]

    new_vx, new_vy = start_vx, 0

    return snake1, snake, eat_me, eat_me_list, pos_list, new_vx, new_vy

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

# Some properties of the snake
width = 15
start_vx = width

snake1, snake, eat_me, eat_me_list, pos_list, new_vx, new_vy = game_setup(width, start_vx)

# Define the fonts for text
font = pygame.font.Font(None, 30)
font_big = pygame.font.Font(None, 40)

try:
    score_file = open("snake_score.txt", "r")
    score_l = score_file.readline()
    score_file.close()
    high_score = int(score_l)
    print("High score loaded.")
except:
    high_score = 0
    print("No high score found.")

score = 0

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
            new_vy = -1 * start_vx
            new_vx = 0
        if event.key == pygame.K_DOWN:
            new_vy = start_vx
            new_vx = 0
        if event.key == pygame.K_LEFT:
            new_vy = 0
            new_vx = -1 * start_vx
        if event.key == pygame.K_RIGHT:
            new_vy = 0
            new_vx = start_vx

    # Show the time that has gone by and write the number of things eaten to the board and the time taken
    time = int(pygame.time.get_ticks())  # milliseconds
    time /= 1000    # seconds

    score_text = font.render("Score: %d" % score, True, BLACK)
    time_text = font.render("Time: %d seconds" % int(time), True, BLACK)
    screen.blit(score_text, [size[0]-200, 0])   # Put the image of the text on the screen
    screen.blit(time_text, [size[0]-200, 20])

    # Set the movement of the head of the snake and append the past movements to a list
    curr_vx, curr_vy = snake1.get_velocity()
    pos_list.append([curr_vx, curr_vy])
    snake1.set_velocity(new_vx, new_vy)

    # Move each part of the snake using the memory of movements
    for sn in snake:
        if sn.chain_number != 0:
            sn.set_velocity(pos_list[-1*sn.chain_number][0], pos_list[-1*sn.chain_number][1])

    # Ensure that the list does not grow in size
    if len(pos_list) == snake1.number_of_chains+1:
        pos_list = pos_list[1:]

    # Check if there exists already something to eat. If no, then make one that is randomly placed
    if not eat_me:
        X = random.random()*(size[0] - width/2.) + width/2.
        Y = random.random()*(size[1] - width/2.) + width/2.
        eat_me = MovingBoxSprite(x=X, y=Y, width=width, height=width, colour=RED, vx=0, vy=0, bounds=size)
        eat_me_list.add(eat_me)

    # Check if the head of the snake sprite has collided with the eatable sprite
    did_i_eat_list = pygame.sprite.spritecollide(snake1, eat_me_list, True)

    # Collision
    if did_i_eat_list:

        # Set false so that next tick it generates a new eatable
        eat_me = False

        # Make extra chain on the snake
        tmp = snake1
        # Look for the last chain in the snake
        for sn in snake:
            if sn.chain_number > tmp.chain_number:
                tmp = sn

        # Calculate its position and trajectory to place it at the right place with respect to the last sprite
        X_new = tmp.rect.x
        Y_new = tmp.rect.y
        VX, VY = tmp.get_velocity()

        # Update the book keeping numbers of the snake
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

        # Generate new snake piece and add to sprite group
        new_snake = MovingBoxSprite(x=X_new, y=Y_new, width=width, height=width, colour=BLUE, vx=VX, vy=VY,
                                    bounds=size, chain_number=NUM+1)
        snake.add(new_snake)

        # Increment the score to show that an eatable occurred
        score += 1

    # Move all the pieces of the snake
    for sn in snake:
        sn.move()

        # Did the snake hit the wall?
        if sn.get_hit():
            # If it hits the wall we want to pause the game and reset everything to the beginning status
            if score > high_score:
                high_score = score

            text_your_score = font_big.render("Your score: %d, High score: %d" % (score, high_score), True, BLACK)
            screen.blit(text_your_score, [50., 50.])
            pygame.display.flip()

            score = 0
            time = 0

            pygame.time.wait(1000)
            snake1, snake, eat_me, eat_me_list, pos_list, new_vx, new_vy = game_setup(width, start_vx)

            break

    # Draw to the screen
    snake.draw(screen)
    eat_me_list.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.

try:
    print("Saved high score.")
    score_out = open("snake_score.txt", "w")
    score_out.write("%d" % high_score)
    score_out.close()
except:
    print("Failed to save high score.")

pygame.quit()
