# import pygame module in this program
import pygame

# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()

# define the RGB value for white,
# green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

# assigning values to X and Y variable
X = 400
Y = 400

# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))

# set the pygame window name
pygame.display.set_caption('Show Text')

# create a font object.
# 1st parameter is the font file
# which is present in pygame.
# 2nd parameter is size of the font

# create a rectangular object for the
# text surface object
# set the center of the rectangular object.
sizes = []
for i in range(0, 50, 2):
    sizes.append(pygame.font.Font('fonts/Cascadia.ttf', i+1).render('GeeksForGeeks', True, green))

# infinite loop
while True:
	# completely fill the surface object
	# with white color
    display_surface.fill(white)
	# copying the text surface object
	# to the display surface object
	# at the center coordinate.
    j = 0
    for i , t in enumerate(sizes):
        display_surface.blit(t, (0, j))
        j += i
	# iterate over the list of Event objects
	# that was returned by pygame.event.get() method.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
			# deactivates the pygame library
            pygame.quit()
			# quit the program.
            quit()

		# Draws the surface object to the screen.
    pygame.display.update()
