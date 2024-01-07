import pygame
import spritesheet
import math
import random

pygame.init()

# Static variables
WIDTH = 1000
HEIGHT = 800
BACKGROUND_WIDTH = 5000
BACKGROUND_HEIGHT = 5000
PLAYER_WIDTH = 96
PLAYER_HEIGHT = 96
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
# Decide a location for enemy
def enemy_location():
    square_top_left_x = 0
    square_top_left_y = 0
    square_bottom_right_x = WIDTH
    square_bottom_right_y = HEIGHT
    while True:
        # Generate random x and y coordinates outside the square
        x = random.uniform(square_top_left_x - 100, square_bottom_right_x + 100)
        y = random.uniform(square_top_left_y - 100, square_bottom_right_y + 100)
        
        # Check if the generated point is outside the square
        if x < square_top_left_x or x > square_bottom_right_x or y < square_top_left_y or y > square_bottom_right_y:
            return x, y

# Initial movement speed (coefficient 0.707)
speed = 100
speed_linear = 4
speed_diagonal = 2.828

# Load sprite sheet image
sprite_sheet_image = pygame.image.load('images/spritesheet.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

# Load enemy sprite sheet
enemy_sprite_sheet_image = pygame.image.load('images/enemy1.png').convert_alpha()
enemy_sprite_sheet = spritesheet.SpriteSheet(enemy_sprite_sheet_image)



# Create animation list
animation_list = []
#animation types
animation_steps = [4, 4, 4, 4]
last_update = pygame.time.get_ticks()
animation_cooldown = 100
action = 0
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 64, 64, 2, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

# Enemy animation list 
enemy_animation_list = []
enemy_animation_steps = [6, 6, 7, 6]
enemy_action = 0
enemy_last_update = pygame.time.get_ticks()
enemy_animation_cooldown = 100
enemy_frame = 0
enemy_step_counter = 0

for enemy_animation in enemy_animation_steps:
    temp_img_list2 = []
    for _ in range(enemy_animation):
        temp_img_list2.append(enemy_sprite_sheet.get_image(enemy_step_counter, 24, 24, 4, BLACK))
        enemy_step_counter += 1
    enemy_animation_list.append(temp_img_list2)

# Create black background surface
black_background = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
black_background.fill(BLACK)

# Getting the enemy location
enemy_coordinate = enemy_location()
enemy_icon_x = enemy_coordinate[0]
enemy_icon_y = enemy_coordinate[1]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
    # Update enemy animation
    enemy_current_time = pygame.time.get_ticks()
    if enemy_current_time - enemy_last_update >= enemy_animation_cooldown:
        enemy_frame += 1
        enemy_last_update = enemy_current_time
        if enemy_frame >= len(enemy_animation_list[enemy_action]):
            enemy_frame = 0
    # Move the icon based on the pressed keys
    if keys[pygame.K_w] and icon_y > 0:
        icon_y -= speed
        action = 3
    if keys[pygame.K_s] and icon_y < HEIGHT - PLAYER_HEIGHT:
        icon_y += speed
        action = 0
    if keys[pygame.K_d] and icon_x < WIDTH - PLAYER_WIDTH:
        icon_x += speed
        action = 2
    if keys[pygame.K_a] and icon_x > 0:
        icon_x -= speed
        action = 1
    if sum(keys) == 0:
        frame = 0

    # Calculate the camera offset to keep the icon centered
    camera_x = icon_x - (WIDTH / 2) + (PLAYER_WIDTH/2)
    camera_y = icon_y - (HEIGHT / 2) + (PLAYER_HEIGHT/2)

    # Draw the BLACK background centered
    screen.blit(black_background, (camera_x - (BACKGROUND_WIDTH/2), camera_y - (BACKGROUND_HEIGHT/2)))

    # Draw the GRASS background with the camera offset
    screen.blit(background_image, (-camera_x, -camera_y))


    # Draw the ICON at the new position
    screen.blit(animation_list[action][frame], (icon_x - camera_x, icon_y - camera_y))

    #Draw ENEMY icon
    screen.blit(enemy_animation_list[enemy_action][enemy_frame], (enemy_icon_x - camera_x, enemy_icon_y - camera_y))

    #Enemy movement
    if icon_x > enemy_icon_x:
        enemy_icon_x += speed/2
        enemy_action = 1
    if icon_x < enemy_icon_x:
        enemy_icon_x -= speed/2
        enemy_action = 3
    if icon_y > enemy_icon_y:
        enemy_icon_y += speed/2
    if icon_y < enemy_icon_y:
        enemy_icon_y -= speed/2

    # FPS counter
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (10, 10))

    pygame.display.update()
    
    # FPS limitation
    clock.tick(FPS)

# Quit pygame outside the loop
pygame.quit()
