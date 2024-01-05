import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 800
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

# Initial movement speed
speed = 4

sprite_sheet_image = pygame.image.load('images/spritesheet.png').convert_alpha()

#Character sprite background
BLACK = (0, 0, 0)

#Character sprite
def get_image(sheet, width, height, scale, colour, position):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (position * 64 , 64, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image

#Getting a certain character animation from sprite
frame_0 = get_image(sprite_sheet_image, 64, 64, 5, BLACK, 0)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the keys that are currently pressed
    keys = pygame.key.get_pressed()

    # Adjust speed based on linear or diagonal movement
    if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
        speed = 2.828  # Reduce speed for diagonal movement
    else:
        speed = 4  # Reset speed for non-diagonal movement

    # Move the icon based on the pressed keys
    if keys[pygame.K_w] and icon_y > 0:
        icon_y -= speed
    if keys[pygame.K_a] and icon_x > 0:
        icon_x -= speed
    if keys[pygame.K_s] and icon_y < HEIGHT - 100:
        icon_y += speed
    if keys[pygame.K_d] and icon_x < WIDTH - 100:
        icon_x += speed

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw the icon at the new position
    screen.blit(pygame.transform.scale(icon, (100, 100)), (icon_x, icon_y))

    screen.blit(frame_0, (0, 0))

    pygame.display.update()

# Quit pygame outside the loop
pygame.quit()