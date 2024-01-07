import pygame
import spritesheet

def set_static_variables():
    global WIDTH, HEIGHT, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, FPS, speed, speed_linear, speed_diagonal
    WIDTH, HEIGHT = 1000, 800
    BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 5000, 5000
    PLAYER_WIDTH, PLAYER_HEIGHT = 144, 144
    FPS = 60
    speed = 4 # Coefficient 0.707
    speed_linear = 4
    speed_diagonal = 2.828


def set_color_codes():
    global BLACK, WHITE, RED, GREEN, BLUE, MAGENTA, YELLOW
    BLACK, WHITE = (0, 0, 0), (255, 255, 255)
    RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
    MAGENTA, YELLOW = (255, 0, 255), (255, 255, 0)

def set_basic_settings():
    global screen, background_surface, icon, clock, font, running, icon_x, icon_y
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background_surface = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("ROGUELIKE STUFF")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40) # Font for FPS counter
    running = True
    icon_x, icon_y = (screen.get_width() - PLAYER_WIDTH) / 2, (screen.get_height() - PLAYER_HEIGHT) / 2

def load_images():
    global background_image, sprite_sheet, black_background
    background_image = pygame.image.load('images/grass_bg.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    sprite_sheet_image = pygame.image.load('images/player.png').convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
    black_background = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
    black_background.fill(BLACK)

def create_animation_list():
    global animation_list, action, frame, step_counter, last_update, animation_cooldown, last_lift_up
    animation_list = []
    animation_steps = [6, 6, 6, 6, 6, 6, 6, 6]
    last_update = pygame.time.get_ticks()
    animation_cooldown = 150
    action, frame, step_counter = 4, 0, 0
    last_lift_up = None

    for animation in animation_steps:
        temp_img_list = []
        for _ in range(animation):
            temp_img_list.append(sprite_sheet.get_image(step_counter, 48, 48, 3, BLACK))
            step_counter += 1
        animation_list.append(temp_img_list)

def initialize_game():
    pygame.init()
    set_static_variables()
    set_color_codes()
    set_basic_settings()
    load_images()
    create_animation_list()

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
