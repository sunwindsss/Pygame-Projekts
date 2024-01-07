import pygame
import spritesheet

def set_static_variables():
    """
    Initializes some basic game variables.
    """
    global WIDTH, HEIGHT, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, FPS, speed, speed_linear, speed_diagonal
    WIDTH, HEIGHT = 1000, 800
    BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 5000, 5000 # For the black background
    PLAYER_WIDTH, PLAYER_HEIGHT = 144, 144 # Attached to some settings in regards to player location on screen
    FPS = 60 # Framerate value for game
    speed = 4
    speed_linear = 4
    speed_diagonal = 2.828 # Coefficient 0.707 in regards to linear speed


def set_color_codes():
    """
    Initializes global color code variables.
    """
    global BLACK, WHITE, RED, GREEN, BLUE, MAGENTA, YELLOW
    BLACK, WHITE = (0, 0, 0), (255, 255, 255)
    RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)
    MAGENTA, YELLOW = (255, 0, 255), (255, 255, 0)

def set_basic_settings():
    """
    Initializes basic settings for the game.

    Global variables:
        screen: Pygame display surface
        background_surface: Pygame surface for background
        icon: Pygame surface for the game icon
        clock: Pygame clock for controlling the frame rate
        font: Font for the FPS counter
        running: Game status variable (True if the game is running, False if it's not)
        icon_x, icon_y: Initial coordinates of the player icon
    """
    global screen, background_surface, icon, clock, font, running, icon_x, icon_y
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    background_surface = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("ROGUELIKE STUFF")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    running = True
    icon_x, icon_y = (screen.get_width() - PLAYER_WIDTH) / 2, (screen.get_height() - PLAYER_HEIGHT) / 2 

def load_images():
    """
    Load and initialize game images (backgrounds, spritesheets, etc.).

    Global variables:
        background_image: Surface for the game background
        sprite_sheet: SpriteSheet object for managing player sprite animations
        black_background: Surface for black background (temporary)
    """
    global background_image, sprite_sheet, black_background
    background_image = pygame.image.load('images/grass_bg.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    sprite_sheet_image = pygame.image.load('images/player.png').convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
    black_background = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
    black_background.fill(BLACK)

def create_animation_list():
    """
    Creates a list of sprite animations for the player
    based on the number of steps in each animation.
    Extracts images from the sprite sheet for each animation sequence.
    """
    global animation_list, action, frame, step_counter, last_update, animation_cooldown, last_lift_up
    animation_list = []
    animation_steps = [6, 6, 6, 6, 6, 6, 6, 6]
    last_update = pygame.time.get_ticks() # Controls animation speed
    animation_cooldown = 150
    action = 4 # Animation that will be set as default when game starts
    frame = 0
    step_counter = 0 # Each step is one frame in the animation
    last_lift_up = None

    # Splits the spritesheet into frames
    for animation in animation_steps:
        temp_img_list = []
        for _ in range(animation):
            temp_img_list.append(sprite_sheet.get_image(step_counter, 48, 48, 3, BLACK))
            step_counter += 1
        animation_list.append(temp_img_list)

def initialize_game():
    """
    Initializes important game functions.
    """
    pygame.init()
    set_static_variables()
    set_color_codes()
    set_basic_settings()
    load_images()
    create_animation_list()

def handle_events():
    """
    Iterates through all Pygame events, such as key presses or closing the game window,
    and updates global variables. 
    
    Handles the QUIT event and KEYUP (last key lifted) event.

    Global variables:
        running: Game status
        last_lift_up: The last key that was released
    """
    global running, last_lift_up
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            last_lift_up = event.key

def update_animation():
    """
    Advances the animation frame based on a specified cooldown time.
    Ensures that the animation frames cycle through the available frames for
    the current action. The animation updates are synchronized with the game's time.
    """
    global frame, last_update, animation_cooldown, action
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

def move_icon():
    """
    Moves the player based on keyboard inputs.
    Adjusts animations based on keyboard inputs.

    Updates the player's position based on the keys pressed,
    adjusting the speed for diagonal or linear movement. 
    Determines the appropriate animation sequence to use based on the direction of movement.
    """
    global icon_x, icon_y, action
    keys = pygame.key.get_pressed()

    # Adjust speed based on linear or diagonal movement
    if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
        speed = speed_diagonal  # Reduce speed for diagonal movement
    else:
        speed = speed_linear  # Adjust speed for non-diagonal movement

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
    """
    Moves the camera by adjusting coordinates each frame.
    Updates global variables `camera_x` and `camera_y` to determine
    the offset needed for the camera to follow the player while staying centered.
    """
    global camera_x, camera_y
    camera_x = icon_x - (WIDTH / 2) + (PLAYER_WIDTH / 2)
    camera_y = icon_y - (HEIGHT / 2) + (PLAYER_HEIGHT / 2)

def draw_elements():
    """
    Uses Pygame's `blit` method to draw different elements on the screen,
    including the black background, game background, and the current frame of player animation.
    The drawing is adjusted based on the calculated camera offset.
    """
    screen.blit(black_background, (camera_x - (BACKGROUND_WIDTH / 2), camera_y - (BACKGROUND_HEIGHT / 2)))
    screen.blit(background_image, (-camera_x, -camera_y))
    screen.blit(animation_list[action][frame], (icon_x - camera_x, icon_y - camera_y))

def draw_fps_counter():
    """
    Renders the current frames per second (FPS) on the screen using
    the specified font and displays it at the top-left corner of the game window.
    """
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (10, 10))

def main_loop():
    """
    Runs the main game loop and processes game events.
    The loop continues until the global variable `running` becomes False, and then quits the game.
    """
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

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    # Initializes the game and starts running the main game loop
    initialize_game()
    main_loop()
