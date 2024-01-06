import pygame
import spritesheet

pygame.init()

# Statiskie mainīgie
WIDTH = 1000
HEIGHT = 800
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

# Pamata iestatījumi saistībā ar spēles logu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_surface = pygame.Surface((WIDTH, HEIGHT))
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("ROGUELIKE STUFF")

# Pulkstenis spēlei (object), lai regulētu FPS
clock = pygame.time.Clock()

# Fonts FPS skaitītājam
font = pygame.font.Font(None, 40)

# Load background image
background_image = pygame.image.load('images/grass_bg.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Spēles statuss
running = True

# Initial position of the icon
icon_x = (screen.get_width() - PLAYER_WIDTH) / 2
icon_y = (screen.get_height() - PLAYER_HEIGHT) / 2

# Initial movement speed (coefficient 0.707)
speed = 4
speed_linear = 4
speed_diagonal = 2.828

sprite_sheet_image = pygame.image.load('images/doux.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

#create animation list
animation_list = []
animation_steps = [4, 6, 3, 4]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 75
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 4, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

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

    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0


    #Move the icon based on the pressed keys
    if keys[pygame.K_w] and icon_y > 0:
        icon_y -= speed
        action = 1
    if keys[pygame.K_a] and icon_x > 0:
        icon_x -= speed
        action = 1
    if keys[pygame.K_s] and icon_y < HEIGHT - PLAYER_HEIGHT:
        icon_y += speed
        action = 1
    if keys[pygame.K_d] and icon_x < WIDTH - PLAYER_WIDTH:
        icon_x += speed
        action = 1
    if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
        action = 0
        frame = 0

    # Calculate the camera offset to keep the icon centered
    camera_x = icon_x - (WIDTH / 2) + (PLAYER_WIDTH/2)
    camera_y = icon_y - (HEIGHT / 2) + (PLAYER_HEIGHT/2)

    # Draw the background with the camera offset
    screen.blit(background_image, (-camera_x, -camera_y))

    # Draw the icon at the new position
    # screen.blit(pygame.transform.scale(icon, (PLAYER_WIDTH, PLAYER_HEIGHT)), (icon_x - camera_x, icon_y - camera_y))
    screen.blit(animation_list[action][frame], (icon_x - camera_x, icon_y - camera_y))

    # FPS counter
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, BLACK)
    screen.blit(fps_text, (10, 10))
    
    pygame.display.update()

    # FPS limitācija
    clock.tick(FPS)

# Quit pygame outside the loop
pygame.quit()