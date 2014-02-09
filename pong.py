"""
 Pong game.

 Uses pygame libraries and followed a guide given by  http://programarcadegames.com/

 Left bat is controlled by a joystick.
 Right bat is controlled by the UP and DOWN arrow keys.

 Scoring will continue forever.
 Can have as many balls as you want by changing the variable: number_of_balls
"""

import pygame
import random

number_of_balls = 0

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

pygame.display.set_caption("Pong")
background_image = pygame.image.load("pong/Bhaskar_A..jpg").convert()
screen.blit(background_image, [0, 0])

click_sound = pygame.mixer.Sound("pong/click.wav")
# pygame.mixer.music.load("pong/track.mp3")
# pygame.mixer.music.play()

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

ball_list = pygame.sprite.Group()
for i in range(0, number_of_balls):
    y = random.random()*size[1]
    ball_sprite = MovingBoxSprite(x=60, y=y, width=20, height=20, colour=RED, vx=10, vy=10, bounds=size)
    ball_list.add(ball_sprite)

bat1_sprite = MovingBoxSprite(x=10, y=size[1]/2-50, width=30, height=100, colour=WHITE, edge_behaviour=0, bounds=size)
bat2_sprite = MovingBoxSprite(x=660, y=size[1]/2-50, width=30, height=100, colour=WHITE, edge_behaviour=0, bounds=size)
bat_list = pygame.sprite.Group()
bat_list.add(bat1_sprite)
bat_list.add(bat2_sprite)

font = pygame.font.Font(None, 50)

left_score, right_score = 0, 0
x_coord1, x_coord2, y_coord1, y_coord2 = 0, 0, 0, 0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # If user clicked close
            done = True     # Flag that we are done so we exit this loop

    # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
    screen.blit(background_image, [190, 0])

    # JOYSTICK INPUT
    # PLAYER 1
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
        horizontal_axis_pos = my_joystick.get_axis(0)
        vertical_axis_pos = my_joystick.get_axis(1)
        # Move x according to the axis. We multiply by 10 to speed up the movement.
        x_coord1 = int(horizontal_axis_pos * 10)
        y_coord1 = int(vertical_axis_pos * 10)

    # KEYBOARD INPUT
    # PLAYER 2
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
    # User let up on a key
    if event.type == pygame.KEYUP:
        # If it is an arrow key, reset vector back to zero
        if event.key == pygame.K_UP:
            y_coord2 = 0
        if event.key == pygame.K_DOWN:
            y_coord2 = 0

    # Score board
    line = pygame.draw.rect(screen, WHITE, [size[0]/2, 0, 2, size[1]], 0)

    text_left = font.render("%d" % left_score, True, WHITE)
    text_right = font.render("%d" % right_score, True, WHITE)
    text_dx = 100
    screen.blit(text_left, [size[0]/2 - text_dx, 0])   # Put the image of the text on the screen
    screen.blit(text_right, [size[0]/2 + text_dx, 0])   # Put the image of the text on the screen

    bat1_sprite.set_velocity(x_coord1, y_coord1)
    bat2_sprite.set_velocity(x_coord2, y_coord2)

    # Check for scoring
    for sprite in ball_list:
        # Check if it hits a bat
        blocks_hit_list = pygame.sprite.spritecollide(sprite, bat_list, False)

        if blocks_hit_list:
            vx, vy = sprite.get_velocity()
            sprite.set_velocity(-1*vx, vy)

        if sprite.rect.x < bat1_sprite.get_width():
        # click_sound.play()
            right_score += 1
            vx, vy = sprite.get_velocity()
            sprite.set_velocity(-1*abs(vx), -1*abs(vy))
            y = random.random()*size[1]
            sprite.reset_position(x=600, y=y)

        elif sprite.rect.x + sprite.get_width() > bat2_sprite.rect.x+10:
            left_score += 1
            vx, vy = sprite.get_velocity()
            sprite.set_velocity(abs(vx), abs(vy))
            y = random.random()*size[1]
            sprite.reset_position(x=60, y=y)

        else:
            sprite.move()

    for sprite in bat_list:
        sprite.move()

    # Draw to the screen
    ball_list.draw(screen)
    bat_list.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()