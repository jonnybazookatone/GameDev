"""
 Pacman game based on old arcade games

  Uses pygame libraries and material from the guide given by  http://programarcadegames.com/

  Pacman is controlled by the LEFT, RIGHT, UP and DOWN arrow keys.

  High scores will be saved in a text file and loaded upon launch of the game.

"""

import pygame
from sprites import CanvasProperties

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

# Define the fonts for text
font = pygame.font.Font(None, 30)
font_big = pygame.font.Font(None, 40)

start_vx = 0

CP = CanvasProperties()





# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():    # User did something
        if event.type == pygame.QUIT:   # If user clicked close
            done = True     # Flag that we are done so we exit this loop

    # --- Drawing code should go here
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(CP.colours["WHITE"])
    pacman_image = pygame.image.load("pacman/blinky.jpg").convert()
    screen.blit(pacman_image, [0, 0])
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

    time_text = font.render("Time: %d seconds" % int(time), True, CP.colours["BLACK"])
    screen.blit(time_text, [size[0]-200, 20])

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.

# try:
#     print("Saved high score.")
#     score_out = open("snake_score.txt", "w")
#     score_out.write("%d" % high_score)
#     score_out.close()
# except IOError:
#     print("Failed to save high score.")

pygame.quit()
