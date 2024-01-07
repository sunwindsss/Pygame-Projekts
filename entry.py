import pygame
import spritesheet

def initialize_game():
    pygame.init()

    # Static variables
    global WIDTH, HEIGHT, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, FPS
    WIDTH = 1000
    HEIGHT = 800
    BACKGROUND_WIDTH = 5000
    BACKGROUND_HEIGHT = 5000
    PLAYER_WIDTH = 144
    PLAYER_HEIGHT = 144
    FPS = 60

    # Color codes
    global BLACK, WHITE, RED, GREEN, BLUE, MAGENTA, YELLOW
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    MAGENTA = (255, 0, 255)
    YELLOW = (255, 255, 0)

    # Basic settings related to the game window
    global screen, background_surface, icon, clock, font, background_image, running, icon_x, icon_y
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
    global speed, speed_linear, speed_diagonal, sprite_sheet, animation_list, action, frame, step_counter, last_update, animation_cooldown, last_lift_up
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
    # animation type list 0 - 3 is walking and 4 - 7 is idle animations
    animation_steps = [6, 6, 6, 6, 6, 6, 6, 6]
    last_update = pygame.time.get_ticks()
    animation_cooldown = 150
    # animation that will be set as default when the game starts
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
    global black_background
    black_background = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
    black_background.fill(BLACK)

def handle_events():
    global running, last_lift_up
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            last_lift_up = event.key

def update_animation():
    global frame, last_update, animation_cooldown, action
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

def move_icon():
    global icon_x, icon_y, action
    keys = pygame.key.get_pressed()

    # Adjust speed based on linear or diagonal movement
    if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
        speed = speed_diagonal  # Reduce speed for diagonal movement
    else:
        speed = speed_linear  # Reset speed for non-diagonal movement

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

    if sum(keys) == 0:
        if last_lift_up == pygame.K_w:
            action = 7
        elif last_lift_up == pygame.K_s:
            action = 4
        elif last_lift_up == pygame.K_a:
            action = 5
        elif last_lift_up == pygame.K_d:
            action = 6

def calculate_camera_offset():
    global camera_x, camera_y
    camera_x = icon_x - (WIDTH / 2) + (PLAYER_WIDTH / 2)
    camera_y = icon_y - (HEIGHT / 2) + (PLAYER_HEIGHT / 2)

def draw_elements():
    screen.blit(black_background, (camera_x - (BACKGROUND_WIDTH / 2), camera_y - (BACKGROUND_HEIGHT / 2)))
    screen.blit(background_image, (-camera_x, -camera_y))
    screen.blit(animation_list[action][frame], (icon_x - camera_x, icon_y - camera_y))

def draw_fps_counter():
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (10, 10))

def main_loop():
    global running
    while running:
        handle_events()
        update_animation()
        move_icon()
        calculate_camera_offset()
        draw_elements()
        draw_fps_counter()

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    initialize_game()
    main_loop()
