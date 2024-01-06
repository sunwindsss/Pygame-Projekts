import pygame
import spritesheet

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
icon_x = (screen.get_width() - 96) // 2
icon_y = (screen.get_height() - 96) // 2

# Initial movement speed
speed = 4

#Character sprite background
BLACK = (0, 0, 0)

sprite_sheet_image = pygame.image.load('images/doux.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

#create animation list
animation_list = []
animation_steps = [4, 6, 3, 4]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 100
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 4, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

while running:

    # Get the keys that are currently pressed
    keys = pygame.key.get_pressed()

    # Adjust speed based on linear or diagonal movement
    if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
        speed = 2.828  # Reduce speed for diagonal movement
    else:
        speed = 4  # Reset speed for non-diagonal movement

    # Draw the background
    screen.blit(background_image, (0, 0))

    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    #mans movement variants

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_w and icon_y > 0:
        #         icon_y -= speed
        #         action = 1
        #     if event.key == pygame.K_a and icon_x > 0:
        #         icon_x -= speed
        #         action = 1
        #     if event.key == pygame.K_s and icon_y < HEIGHT - 96:
        #         icon_y += speed
        #         action = 1
        #     if event.key == pygame.K_d and icon_x < WIDTH - 96:
        #         icon_x += speed
        #         action = 1
            # if not event.key == pygame.K_w and not event.key == pygame.K_a and not event.key == pygame.K_s and not event.key == pygame.K_d:
            #     action = 0
            #     frame = 0

        # if event.type == pygame.KEYUP:
        #     action = 0
        #     frame = 0

    #Move the icon based on the pressed keys
    if keys[pygame.K_w] and icon_y > 0:
        icon_y -= speed
        action = 1
    if keys[pygame.K_a] and icon_x > 0:
        icon_x -= speed
        action = 1
    if keys[pygame.K_s] and icon_y < HEIGHT - 96:
        icon_y += speed
        action = 1
    if keys[pygame.K_d] and icon_x < WIDTH - 96:
        icon_x += speed
        action = 1
    if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
        action = 0
        frame = 0
    # if event.type == pygame.KEYUP:
    #     action = 0
    #     frame = 0
    # if sum(keys) == 0:
    #     action = 0
    #     frame = 0


    # Draw the player at the new position
    screen.blit(animation_list[action][frame], (icon_x, icon_y))

    pygame.display.update()

# Quit pygame outside the loop
pygame.quit()