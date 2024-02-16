import pygame, sys, keyboard
p = [] # '1234567890-=qwertyuiop[]asdfghjkl;'#\zxcvbnm,./'
for i in '!"£$%^&*()_+QWERTYUIOP{}ASDFGHJKL:@~|ZXCVBNM<>?':
    p.append(i)
print(p)



'''KEY_VALUES = {pygame.K_0: '0'}
def get_pressed():
    ke = pygame.key.get_pressed()
# Initialize Pygame
pygame.init()
keys = 123567890-=qwertyuiop[]asdfghjkl;'#\zxcvbnm,./
# Set up the window
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Pygame Window")
#keys = []
# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    for i in keys:
        if keyboard.is_pressed(i):
            print(i)
    ke = pygame.key.get_pressed()
    for i in range(len(ke)):
        if ke[pygame.K_0]:
            print('hi')

    # Add your game logic and drawing code here

    # Update the display
    pygame.display.flip()'''