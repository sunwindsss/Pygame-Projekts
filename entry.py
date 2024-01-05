import pygame

pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_surface = pygame.Surface((WIDTH, HEIGHT))
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

# Load background image
background_image = pygame.image.load('images/grass_bg.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

running = True

# Initial position of the icon
icon_x = (screen.get_width() - 100) // 2
icon_y = (screen.get_height() - 100) // 2

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys that are currently pressed
    keys = pygame.key.get_pressed()

    # Move the icon based on the pressed keys
    if keys[pygame.K_w] and icon_y > 0:
        icon_y -= 5
    if keys[pygame.K_a] and icon_x > 0:
        icon_x -= 5
    if keys[pygame.K_s] and icon_y < HEIGHT - 100:
        icon_y += 5
    if keys[pygame.K_d] and icon_x < WIDTH - 100:
        icon_x += 5

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw the icon at the new position
    screen.blit(pygame.transform.scale(icon, (100, 100)), (icon_x, icon_y))

    pygame.display.update()

# Quit pygame outside the loop
pygame.quit()
