import pygame
import spritesheet

pygame.init()

# Static variables
WIDTH = 1000
HEIGHT = 800
BACKGROUND_WIDTH = 5000
BACKGROUND_HEIGHT = 5000
PLAYER_WIDTH = 144
PLAYER_HEIGHT = 144
FPS = 60

# Color codes
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# Basic settings related to the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_surface = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("ROGUELIKE STUFF")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Font for the FPS counter
font = pygame.font.Font(None, 40)

# Load background image
background_image = pygame.image.load('images/grass_bg.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Game status
running = True

# Initial position of the icon
icon_x = (screen.get_width() - PLAYER_WIDTH) / 2
icon_y = (screen.get_height() - PLAYER_HEIGHT) / 2

# Initial movement speed (coefficient 0.707)
speed = 4
speed_linear = 4
speed_diagonal = 2.828

# Load sprite sheet image
sprite_sheet_image = pygame.image.load('images/player.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# Create animation list
animation_list = []
#animation type list 0 - 3 is walking and 4 - 7 is idle animations
animation_steps = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
last_update = pygame.time.get_ticks()
animation_cooldown = 150
#animation that will be set as default when game starts
action = 4
frame = 0
step_counter = 0

last_lift_up = None

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 48, 48, 3, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

# Create black background surface
black_background = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
black_background.fill(BLACK)

while running:

    # Get the keys that are currently pressed
    keys = pygame.key.get_pressed()

    # Adjust speed based on linear or diagonal movement
    if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
        speed = speed_diagonal  # Reduce speed for diagonal movement
    else:
        speed = speed_linear  # Reset speed for non-diagonal movement

    # Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    # Move the icon based on the pressed keys and use appropriate animations
    if keys[pygame.K_s] and icon_y < HEIGHT - PLAYER_HEIGHT:
        icon_y += speed
        action = 0
    if keys[pygame.K_d] and icon_x < WIDTH - PLAYER_WIDTH:
        icon_x += speed
        action = 2
    if keys[pygame.K_a] and icon_x > 0:
        icon_x -= speed
        action = 1
    if keys[pygame.K_w] and icon_y > 0:
        icon_y -= speed
        action = 3
    if keys[pygame.K_k]:
        if last_lift_up == pygame.K_w:
            action = 11
        elif last_lift_up == pygame.K_s:
            action = 8
        elif last_lift_up == pygame.K_a:
            action = 9
        elif last_lift_up == pygame.K_d:
            action = 10
    # player model uses idle animations according to key released
    if sum(keys) == 0 and last_lift_up == pygame.K_w:
        action = 7
    if sum(keys) == 0 and last_lift_up == pygame.K_s:
        action = 4
    if sum(keys) == 0 and last_lift_up == pygame.K_a:
        action = 5
    if sum(keys) == 0 and last_lift_up == pygame.K_d:
        action = 6

    # Calculate the camera offset to keep the icon centered
    camera_x = icon_x - (WIDTH / 2) + (PLAYER_WIDTH/2)
    camera_y = icon_y - (HEIGHT / 2) + (PLAYER_HEIGHT/2)

    # Draw the BLACK background centered
    screen.blit(black_background, (camera_x - (BACKGROUND_WIDTH/2), camera_y - (BACKGROUND_HEIGHT/2)))

    # Draw the GRASS background with the camera offset
    screen.blit(background_image, (-camera_x, -camera_y))

    # Draw the icon at the new position
    screen.blit(animation_list[action][frame], (icon_x - camera_x, icon_y - camera_y))

    # FPS counter
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (10, 10))

    pygame.display.update()
    
    # FPS limitation
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            last_lift_up = event.key

# Quit pygame outside the loop
pygame.quit()
