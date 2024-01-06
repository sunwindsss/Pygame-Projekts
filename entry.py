import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 800
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_surface = pygame.Surface((WIDTH, HEIGHT))
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("ROGUELIKE STUFF")

# Pulkstenis spēlei (object), lai regulētu FPS
clock = pygame.time.Clock()

# Fonts FPS skaitītājam
font = pygame.font.Font(None, 36)

# Load background image
background_image = pygame.image.load('images/grass_bg.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

running = True

# Initial position of the icon
icon_x = (screen.get_width() - 100) // 2
icon_y = (screen.get_height() - 100) // 2

# Initial movement speed
speed = 4

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

    # FPS counter
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (0, 0, 0))
    screen.blit(fps_text, (10, 10))

    pygame.display.update()

    # FPS limitācija
    clock.tick(FPS)

# Quit pygame outside the loop
pygame.quit()