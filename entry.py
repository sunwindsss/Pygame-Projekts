import pygame
import spritesheet
import random

def set_static_variables():
    """
    Initializes some basic game variables.
    """
    global WIDTH, HEIGHT, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, FPS, speed, speed_linear, speed_diagonal
    WIDTH, HEIGHT = 1000, 800
    BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 100, 100 # Black background size (UNUSED!!)
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
    Load and initialize game images (temporary black background, spritesheets, etc.).

    Global variables:
        sprite_sheet: SpriteSheet object for managing player sprite animations
        black_background: Surface for black background (temporary)
    """
    global sprite_sheet, black_background
    #global background_image # NOT USED ANYMORE
    #background_image = pygame.image.load('images/grass_bg.png') # NOT USED ANYMORE
    #background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) # NOT USED ANYMORE
    sprite_sheet_image = pygame.image.load('images/player.png').convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
    black_background = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT)) # NOT USED ANYMORE
    black_background.fill(BLACK) # NOT USED ANYMORE

def load_background_tiles():
    """
    Loads and scales all background tile images from the 'images' directory.
    Populates the global 'background_tiles' list with each tile image.
    Images 'bg-1.png' to 'bg-10.png' are loaded in that order.

    Global variables:
        background_tiles: List of loaded background tile images.
    """
    global background_tiles
    background_tiles = []
    for i in range(1, 11):
        image = pygame.image.load(f'images/bg-{i}.png').convert()
        image = pygame.transform.scale(image, (WIDTH, HEIGHT))
        background_tiles.append(image)

def select_tile_index():
    """
    Randomly selects an index for a background tile based on predefined probabilities.
    Uses weighted random selection to choose an index, corresponding to a specific background tile.

    Returns:
        integer: The selected tile index.
    """
    chances = [40] + [10] * 4 + [7] * 2 + [3] * 3 # Change probabilities for each image if needed!
    tiles = list(range(10))  # Tile indices from 0 to 9
    return random.choices(tiles, weights=chances, k=1)[0]

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
    global tile_grid
    tile_grid = {}  # Dictionary to keep track of which tiles are loaded
    pygame.init()
    set_static_variables()
    set_color_codes()
    set_basic_settings()
    load_images()
    load_background_tiles()
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
    if keys[pygame.K_s]:
        icon_y += speed
        action = 0
    if keys[pygame.K_d]:
        icon_x += speed
        action = 2
    if keys[pygame.K_a]:
        icon_x -= speed
        action = 1
    if keys[pygame.K_w]:
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

def get_background_tiles():
    """
    Calculates which background tiles are needed based on the player's position.
    The function creates a list of tiles to be drawn, each with its position and
    randomly selected index.
    Eensures that the same tile is not redrawn and maintains a grid of loaded tiles.

    Global variables:
        tile_grid: Dictionary tracking the loaded tiles on the grid.

    Returns:
        list: List of tuples, where each tuple contains the x and y coordinates of the tile
        and the index of the tile image to be used.
    """
    global tile_grid
    tiles = []
    start_x = int(icon_x // WIDTH) * WIDTH
    start_y = int(icon_y // HEIGHT) * HEIGHT

    for x in range(start_x - WIDTH, start_x + 2 * WIDTH, WIDTH):
        for y in range(start_y - HEIGHT, start_y + 2 * HEIGHT, HEIGHT):
            grid_x, grid_y = x // WIDTH, y // HEIGHT

            # If the tile is not already in the grid, select a new tile
            if (grid_x, grid_y) not in tile_grid:
                tile_index = select_tile_index()
                tile_grid[(grid_x, grid_y)] = tile_index

            tiles.append((x, y, tile_grid[(grid_x, grid_y)]))

    return tiles

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
    Draws the necessary background tiles and the player icon on the screen.
    Fetches the required tiles from 'get_background_tiles' and
    then draws them on the screen. 
    It also places the player icon at its current position.

    Global variables:
        background_tiles: List of loaded background tile images.
        animation_list: List of player animation frames.
        action: Current action (animation) for player.
        frame: Current frame for the player animation.
        icon_x, icon_y: Current x and y coordinates of the player.
        camera_x, camera_y: Current x and y coordinates of the camera.
    """
    tiles = get_background_tiles()
    for tile in tiles:
        x, y, tile_index = tile
        screen.blit(background_tiles[tile_index], (x - camera_x, y - camera_y))

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
