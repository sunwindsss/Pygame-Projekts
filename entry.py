import pygame
import spritesheet
import random

def set_static_variables():
    """
    Initializes some basic game variables.
    """
    global WIDTH, HEIGHT, BACKGROUND_WIDTH, BACKGROUND_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT, FPS, speed, speed_linear, speed_diagonal, MAX_ARROWS, ARROW_SPEED,WIN, last_shot_time
    WIDTH, HEIGHT = 1000, 800
    BACKGROUND_WIDTH, BACKGROUND_HEIGHT = 100, 100 # Black background size (UNUSED!!)
    PLAYER_WIDTH, PLAYER_HEIGHT = 144, 144 # Attached to some settings in regards to player location on screen
    FPS = 60 # Framerate value for game
    WIN = pygame.display.set_mode((WIDTH,HEIGHT))
    MAX_ARROWS = 10 # Max arrows on screen at a time 
    last_shot_time = 0 # Needed to time arrow shots
    ARROW_SPEED = 7
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
    pygame.display.set_caption("IKONIKS -- SPĒLES REŽĪMS!")
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
    global sprite_sheet, black_background, enemy_sprite_sheet1, enemy_sprite_sheet2, enemy_sprite_sheet3, iron_arrow_R, iron_arrow_L, iron_arrow_UP, iron_arrow_DOWN
    global health_pickup_image

    sprite_sheet_image = pygame.image.load('images/player.png').convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

    enemy_sprite_sheet_image1 = pygame.image.load('images/enemy1.png').convert_alpha()
    enemy_sprite_sheet1 = spritesheet.SpriteSheet(enemy_sprite_sheet_image1)

    enemy_sprite_sheet_image2 = pygame.image.load('images/doux_upgrade.png').convert_alpha()
    enemy_sprite_sheet2 = spritesheet.SpriteSheet(enemy_sprite_sheet_image2)

    enemy_sprite_sheet_image3 = pygame.image.load('images/enemy2.png').convert_alpha()
    enemy_sprite_sheet3 = spritesheet.SpriteSheet(enemy_sprite_sheet_image3)

    iron_arrow_R = pygame.image.load('images/iron arrow R.png')
    iron_arrow_L = pygame.image.load('images/iron arrow L.png')
    iron_arrow_UP = pygame.image.load('images/iron arrow UP.png')
    iron_arrow_DOWN = pygame.image.load('images/iron arrow DOWN.png')
    #iron_arrow_R = pygame.transform.scale(iron_arrow_R_image, 64, 64)

    black_background = pygame.Surface((BACKGROUND_WIDTH, BACKGROUND_HEIGHT)) # NOT USED ANYMORE
    black_background.fill(BLACK) # NOT USED ANYMORE

    health_pickup_image = pygame.image.load('images/Item_Black1.png').convert_alpha()
    health_pickup_image = pygame.transform.scale(health_pickup_image, (48, 48))


def load_sound_effects():
    """
    Load and initialize sound effects for the game mode.
    """
    global arrow_shoot, death, enemy_hit, take_potion
    arrow_shoot = pygame.mixer.Sound('sounds/arrow_shoot.wav')
    death = pygame.mixer.Sound('sounds/death.wav')
    enemy_hit = pygame.mixer.Sound('sounds/enemy_hit.wav')
    take_potion = pygame.mixer.Sound('sounds/take_potion.wav')

    take_potion.set_volume(0.3)
    arrow_shoot.set_volume(0.3)
    death.set_volume(0.5)
    enemy_hit.set_volume(0.3)


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

def load_game_over_assets():
    """
    Load images and sounds for the game over screen.
    """
    global gameover_img, mainmenu_imgs, restart_imgs, backquit_sound, start_sound
    gameover_img = pygame.image.load('images/gameover.png').convert_alpha()
    gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))

    # Load button images and rescale them
    mainmenu_imgs = [pygame.transform.scale(pygame.image.load(f'images/mainmenu-{i}.png'), (300, 100)) for i in range(1, 4)]
    restart_imgs = [pygame.transform.scale(pygame.image.load(f'images/restart-{i}.png'), (250, 100)) for i in range(1, 4)]

    backquit_sound = pygame.mixer.Sound('sounds/backquit.ogg')
    start_sound = pygame.mixer.Sound('sounds/start.ogg')

    start_sound.set_volume(0.1)
    backquit_sound.set_volume(0.1)

def game_over_screen():
    """
    Displays the game over screen with interactive buttons.
    """
    global running, score
    mainmenu_rect = pygame.Rect((WIDTH // 2 + 50, HEIGHT // 2 + 280), (300, 100))
    restart_rect = pygame.Rect((WIDTH // 2 - 350, HEIGHT // 2 + 280), (250, 100))

    while True:
        screen.blit(gameover_img, (0, 0))

        font = pygame.font.Font(None, 100)
        score_text = font.render(f"{int(score)}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 + 40, HEIGHT // 2 + 135))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True

        if mainmenu_rect.collidepoint(mouse_pos):
            screen.blit(mainmenu_imgs[1], mainmenu_rect.topleft)
            if mouse_click:
                screen.blit(mainmenu_imgs[2], mainmenu_rect.topleft)
                screen.blit(restart_imgs[0], restart_rect.topleft)
                pygame.display.update()
                pygame.mixer.Channel(5).play(backquit_sound)
                pygame.time.delay(100)  # Delay to see the 'clicking' image
                import start_here  # Import the script containing the main menu
                pygame.mixer.stop()
                start_here.main_menu()  # Call main_menu function from start_here
                break
        else:
            screen.blit(mainmenu_imgs[0], mainmenu_rect.topleft)

        if restart_rect.collidepoint(mouse_pos):
            screen.blit(restart_imgs[1], restart_rect.topleft)
            if mouse_click:
                screen.blit(restart_imgs[2], restart_rect.topleft)
                screen.blit(mainmenu_imgs[0], mainmenu_rect.topleft)
                pygame.display.update()
                pygame.mixer.Channel(4).play(start_sound)
                pygame.time.delay(100)
                start_game()  # Restart the game
                break
        else:
            screen.blit(restart_imgs[0], restart_rect.topleft)

        pygame.display.update()
        clock.tick(FPS)


def create_animation_list():
    """
    Creates a list of sprite animations for the player
    based on the number of steps in each animation.
    Extracts images from the sprite sheet for each animation sequence.
    """
    global animation_list, action, frame, step_counter, last_update, animation_cooldown, last_lift_up, animation_completed
    animation_list = []
    animation_steps = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7]
    last_update = pygame.time.get_ticks() # Controls animation speed
    animation_cooldown = 150
    action = 4 # Animation that will be set as default when game starts
    frame = 0
    step_counter = 0 # Each step is one frame in the animation
    last_lift_up = pygame.K_s
    animation_completed = False

    # Splits the spritesheet into frames
    for animation in animation_steps:
        temp_img_list = []
        for _ in range(animation):
            temp_img_list.append(sprite_sheet.get_image(step_counter, 48, 48, 3, BLACK))
            step_counter += 1
        animation_list.append(temp_img_list)

def create_enemy_animation_list(enemy_sprite_sheet):
    global enemy_animation_list, enemy_action, enemy_frame, enemy_step_counter, enemy_last_update, enemy_animation_cooldown
    enemy_animation_list = []
    enemy_animation_steps = [6]
    enemy_action = 0
    enemy_last_update = pygame.time.get_ticks()
    enemy_animation_cooldown = 100
    enemy_frame = 0
    enemy_step_counter = 0


    for enemy_animation in enemy_animation_steps:
        temp_img_list2 = []
        for _ in range(enemy_animation):
            temp_img_list2.append(enemy_sprite_sheet.get_image(enemy_step_counter, 32, 32, 4, BLACK))
            enemy_step_counter += 1
        enemy_animation_list.append(temp_img_list2)
    
    return enemy_animation_list

def initialize_game():
    """
    Initializes important game functions.
    """
    global tile_grid, animation_list1, animation_list2, animation_list3
    tile_grid = {}  # Dictionary to keep track of which tiles are loaded
    pygame.init()
    set_static_variables()
    set_color_codes()
    set_basic_settings()
    load_images()
    load_sound_effects()
    load_background_tiles()
    load_game_over_assets()
    create_animation_list()
    animation_list1 = create_enemy_animation_list(enemy_sprite_sheet1)
    animation_list2 = create_enemy_animation_list(enemy_sprite_sheet2)
    animation_list3 = create_enemy_animation_list(enemy_sprite_sheet3)

PLAYER_HIT = pygame.USEREVENT + 1
ENEMY_HIT1 = pygame.USEREVENT + 2
ENEMY_HIT2 = pygame.USEREVENT + 3
ENEMY_HIT3 = pygame.USEREVENT + 4

ENEMY_HIT1_MELE = pygame.USEREVENT + 5
ENEMY_HIT2_MELE = pygame.USEREVENT + 6
ENEMY_HIT3_MELE = pygame.USEREVENT + 7

def handle_events():
    """
    Iterates through all Pygame events, such as key presses or closing the game window,
    and updates global variables. 
    
    Handles the QUIT event and KEYUP (last key lifted) event.

    Global variables:
        running: Game status
        last_lift_up: The last key that was released
    """
    global running, last_lift_up, player_health, enemy1_health, enemy2_health, enemy3_health, last_shot_time, current_time, action, frame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            last_lift_up = event.key
        elif event.type == PLAYER_HIT:
            player_health -= 1
        elif event.type == ENEMY_HIT1:
            pygame.mixer.Channel(2).play(enemy_hit)
            enemy1_health -= 25
        elif event.type == ENEMY_HIT2:
            pygame.mixer.Channel(2).play(enemy_hit)
            enemy2_health -= 25
        elif event.type == ENEMY_HIT3:
            pygame.mixer.Channel(2).play(enemy_hit)
            enemy3_health -= 25

        elif event.type == ENEMY_HIT1_MELE:
            enemy1_health -= 1
        elif event.type == ENEMY_HIT2_MELE:
            enemy2_health -= 1
        elif event.type == ENEMY_HIT3_MELE:
            enemy3_health -= 1
        
        if event.type == pygame.KEYDOWN and current_time - last_shot_time >= 400:
            if event.key == pygame.K_SPACE and len(player_arrows_R) < MAX_ARROWS:
                pygame.mixer.Channel(1).play(arrow_shoot)
                arrow_R = pygame.Rect(player.x, player.y + player.height//2 - 2, 10, 5)
                player_arrows_R.append(arrow_R)
                last_shot_time = current_time
            if event.key == pygame.K_SPACE and len(player_arrows_L) < MAX_ARROWS:
                arrow_L = pygame.Rect(player.x, player.y + player.height//2 - 2, 10, 5)
                last_shot_time = current_time
                player_arrows_L.append(arrow_L)
            if event.key == pygame.K_SPACE and len(player_arrows_UP) < MAX_ARROWS:
                arrow_UP = pygame.Rect(player.x + 18, player.y + player.height//2 - 2, 10, 5)
                player_arrows_UP.append(arrow_UP)
                last_shot_time = current_time
            if event.key == pygame.K_SPACE and len(player_arrows_DOWN) < MAX_ARROWS:
                arrow_DOWN = pygame.Rect(player.x + 20, player.y + player.height//2 - 2, 10, 5)
                player_arrows_DOWN.append(arrow_DOWN)
                last_shot_time = current_time
            # if event.key == pygame.K_l: #possibility to end game at any time
            #     print("Death triggered")
            #     frame = 0
            #     action = 12


            
            


def update_animation():
    """
    Advances the animation frame based on a specified cooldown time.
    Ensures that the animation frames cycle through the available frames for
    the current action. The animation updates are synchronized with the game's time.
    """
    global frame, last_update, animation_cooldown, animation_completed, action

    current_time = pygame.time.get_ticks()

    if current_time - last_update >= animation_cooldown:
        if not animation_completed:
            frame += 1
            last_update = current_time
            if frame >= len(animation_list[action]):
                frame = 0
                animation_completed = True

def update_enemy_animation():
    global enemy_frame, enemy_last_update, enemy_animation_cooldown, enemy_action
    # Update enemy animations
    enemy_current_time = pygame.time.get_ticks()
    if enemy_current_time - enemy_last_update >= enemy_animation_cooldown:
        enemy_frame += 1
        enemy_last_update = enemy_current_time
        if enemy_frame >= len(enemy_animation_list[enemy_action]):
            enemy_frame = 0 

def move_icon():
    """
    Moves the player based on keyboard inputs.
    Adjusts animations based on keyboard inputs.

    Updates the player's position based on the keys pressed,
    adjusting the speed for diagonal or linear movement. 
    Determines the appropriate animation sequence to use based on the direction of movement.
    """
    global icon_x, icon_y, player, action, frame, animation_completed, last_shot_time, dead
    keys = pygame.key.get_pressed()

    # Adjust speed based on linear or diagonal movement
    if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
        speed = speed_diagonal  # Reduce speed for diagonal movement
    else:
        speed = speed_linear  # Adjust speed for non-diagonal movement

    # Move the icon based on the pressed keys and use appropriate animations
    if dead == False:
        if keys[pygame.K_s]:
            player.y += speed
            action = 0
            animation_completed = False
        if keys[pygame.K_d]:
            player.x += speed
            action = 2
            animation_completed = False
        if keys[pygame.K_a]:
            player.x -= speed
            action = 1
            animation_completed = False
        if keys[pygame.K_w]:
            player.y -= speed
            action = 3
            animation_completed = False

    if sum(keys) == 0 and last_lift_up != pygame.K_SPACE and dead == False:
        animation_completed = False
        if last_lift_up == pygame.K_w:
            action = 7
        elif last_lift_up == pygame.K_s:
            action = 4
        elif last_lift_up == pygame.K_a:
            action = 5
        elif last_lift_up == pygame.K_d:
            action = 6

    if keys[pygame.K_SPACE] and not keys[pygame.K_w] and not keys[pygame.K_s] and not keys[pygame.K_a] and not keys[pygame.K_d] and dead == False:
        animation_completed = False
        if last_lift_up == pygame.K_w:
            action = 11
        elif last_lift_up == pygame.K_s:
            action = 8
        elif last_lift_up == pygame.K_a:
            action = 9
        elif last_lift_up == pygame.K_d:
            action = 10

    #if player health is zero action 12 is enabled, which is death animation
    if player_health <= 0 and dead == False:
        pygame.mixer.Channel(2).play(death)
        frame = 0 
        action = 12
        dead = True
        print("Player dies")
    
def get_background_tiles():
    """
    Calculates which background tiles are needed based on the player's position.
    The function creates a list of tiles to be drawn, each with its position and
    randomly selected index.
    Ensures that the same tile is not redrawn and maintains a grid of loaded tiles.

    Global variables:
        tile_grid: Dictionary tracking the loaded tiles on the grid.

    Returns:
        list: List of tuples, where each tuple contains the x and y coordinates of the tile
        and the index of the tile image to be used.
    """
    global tile_grid
    tiles = []
    start_x = int(player.x // WIDTH) * WIDTH
    start_y = int(player.y // HEIGHT) * HEIGHT

    for x in range(start_x - WIDTH, start_x + 2 * WIDTH, WIDTH):
        for y in range(start_y - HEIGHT, start_y + 2 * HEIGHT, HEIGHT):
            grid_x, grid_y = x // WIDTH, y // HEIGHT

            # If the tile is not already in the grid, select a new tile
            if (grid_x, grid_y) not in tile_grid:
                tile_index = select_tile_index()
                tile_grid[(grid_x, grid_y)] = tile_index

            tiles.append((x, y, tile_grid[(grid_x, grid_y)]))

    return tiles
# Enemy stuff
def enemy_pathfinding(enemy, player):
    global enemy_action

    # Adjust speed based on linear or diagonal movement
    if ((enemy.x > player.x) or (enemy.x < player.x)) and ((enemy.y > player.y) or (enemy.y < player.y)):
        speed = speed_diagonal  # Reduce speed for diagonal movement
    else:
        speed = speed_linear

    if player.x > enemy.x:
        enemy.x += speed/2
        enemy_action = 0
    if player.x < enemy.x:
        enemy.x -= speed/2
        enemy_action = 0
    if player.y > enemy.y:
        enemy.y += speed/2
    if player.y < enemy.y:
        enemy.y -= speed/2

def enemy_spawn(player):
    square_top_left_x = player.x - 500
    square_top_left_y = player.y - 400
    square_bottom_right_x = player.x + 500
    square_bottom_right_y = player.y + 400
    while True:
        # Generate random x and y coordinates outside the square
        x = random.uniform(square_top_left_x - 100, square_bottom_right_x + 100)
        y = random.uniform(square_top_left_y - 100, square_bottom_right_y + 100)
        
        # Check if the generated point is outside the square
        if x < square_top_left_x or x > square_bottom_right_x or y < square_top_left_y or y > square_bottom_right_y:
            return x, y 

def calculate_camera_offset():
    """
    Moves the camera by adjusting coordinates each frame.
    Updates global variables `camera_x` and `camera_y` to determine
    the offset needed for the camera to follow the player while staying centered.
    """
    global camera_x, camera_y
    camera_x = player.x - (WIDTH / 2) + (PLAYER_WIDTH / 3) - 26
    camera_y = player.y - (HEIGHT / 2) + (PLAYER_HEIGHT / 3) - 26

def draw_elements(enemy1, enemy2, enemy3, enemy_animation_list1, enemy_animation_list2, enemy_animation_list3, player_arrows_R, player_arrows_L, player_arrows_UP, player_arrows_DOWN):

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
    #screen.blit(animation_list[action][frame], (icon_x - camera_x, icon_y - camera_y))
    screen.blit(enemy_animation_list1[enemy_action][enemy_frame], (enemy1.x - camera_x - 26, enemy1.y - camera_y - 55))
    screen.blit(enemy_animation_list2[enemy_action][enemy_frame], (enemy2.x - camera_x - 26, enemy2.y - camera_y - 55))
    screen.blit(enemy_animation_list3[enemy_action][enemy_frame], (enemy3.x - camera_x - 26, enemy3.y - camera_y - 55))
    screen.blit(animation_list[action][frame], (player.x - camera_x - PLAYER_WIDTH/3, player.y - camera_y - PLAYER_HEIGHT/3))
    
    # Arrow image drawing
    for arrow_R in player_arrows_R:
        screen.blit(iron_arrow_R, (arrow_R.x - camera_x -25, arrow_R.y - camera_y -27))
    for arrow_L in player_arrows_L:
        screen.blit(iron_arrow_L, (arrow_L.x - camera_x -25, arrow_L.y - camera_y -27))
    for arrow_UP in player_arrows_UP:
        screen.blit(iron_arrow_UP, (arrow_UP.x - camera_x -25, arrow_UP.y - camera_y - 27))
    for arrow_DOWN in player_arrows_DOWN:
        screen.blit(iron_arrow_DOWN, (arrow_DOWN.x - camera_x -29, arrow_DOWN.y - camera_y -27))
    health_bar.draw(screen)

    # ARROW HITBOX DEBUGGING
    for arrow_R in player_arrows_R:
        #RIGHT ARROW
        pygame.draw.rect(screen, (0, 255, 255), (arrow_R.x - camera_x, arrow_R.y - camera_y, arrow_R.width, arrow_R.height), 2) # Blue
    for arrow_L in player_arrows_L:
        #LEFT ARROW
        pygame.draw.rect(screen, (125, 125, 255), (arrow_L.x - camera_x, arrow_L.y - camera_y, arrow_L.width, arrow_L.height), 2) # Blue
    for arrow_UP in player_arrows_UP:
        #UP ARROW
        pygame.draw.rect(screen, (255, 255, 120), (arrow_UP.x - camera_x, arrow_UP.y - camera_y, arrow_UP.width, arrow_UP.height), 2) # Blue
    for arrow_DOWN in player_arrows_DOWN:
        #DOWN ARROW
        pygame.draw.rect(screen, (255, 0, 255), (arrow_DOWN.x - camera_x, arrow_DOWN.y - camera_y, arrow_DOWN.width, arrow_DOWN.height), 2) # Blue

    #ONLY FOR DEBUGGING ENEMY HITBOXES
    for enemy, enemy_animation_list in [(enemy1, enemy_animation_list1), (enemy2, enemy_animation_list2), (enemy3, enemy_animation_list3)]:
        #screen.blit(enemy_animation_list[enemy_action][enemy_frame], (enemy.x - camera_x-10, enemy.y - camera_y-15))
        pygame.draw.rect(screen, (255, 255, 0), (enemy.x - camera_x, enemy.y - camera_y, enemy.width, enemy.height), 2)

    #DEBUGGING PLAYER HITBOX
    pygame.draw.rect(screen, (0, 255, 0), (player.x - camera_x, player.y - camera_y, player.width, player.height), 2)

    for pickup in health_pickups:
        screen.blit(health_pickup_image, (pickup.x - camera_x, pickup.y - camera_y -10))
        #DEBUGGING PICKUP HITBOXES
        pygame.draw.rect(screen, (255, 0, 0), (pickup.x - camera_x, pickup.y - camera_y, pickup.width, pickup.height), 2)


def generate_health_pickup(x, y):
    """
    Generates a health pickup at the specified coordinates.
    """
    health_pickup = pygame.Rect(x + PLAYER_WIDTH/2 - 60, y + PLAYER_HEIGHT/2 - 60, 48, 40)
    health_pickups.append(health_pickup)

def handle_health_pickups():
    """
    Handles the health pickups, ensuring that player health doesn't go above 100.
    """
    global player_health, take_potion, dead
    if dead == True:
        return
    player_health = min(player_health + 50, 100) if any(player.colliderect(pickup) for pickup in health_pickups) else player_health
    for pickup in health_pickups[:]:
        if player.colliderect(pickup):
            pygame.mixer.Channel(3).play(take_potion)
            health_pickups.remove(pickup)

def draw_fps_counter():
    """
    Renders the current frames per second (FPS) on the screen using
    the specified font and displays it at the top-left corner of the game window.
    """
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    score_text = font.render(f"Score: {int(score)}", True, WHITE)
    screen.blit(fps_text, (10, 10))
    screen.blit(score_text, (10, 45))

def player_damage(player, enemy1, enemy2, enemy3):
    if player.colliderect(enemy1):
        pygame.event.post(pygame.event.Event(PLAYER_HIT))
    if player.colliderect(enemy2):
        pygame.event.post(pygame.event.Event(PLAYER_HIT))
    if player.colliderect(enemy3):
        pygame.event.post(pygame.event.Event(PLAYER_HIT))

def enemy_damage(player, enemy1, enemy2, enemy3):
    if player.colliderect(enemy1):
        pygame.event.post(pygame.event.Event(ENEMY_HIT1_MELE))
    if player.colliderect(enemy2):
        pygame.event.post(pygame.event.Event(ENEMY_HIT2_MELE))
    if player.colliderect(enemy3):
        pygame.event.post(pygame.event.Event(ENEMY_HIT3_MELE))


def handle_arrows_R(player_arrows_R, action):
    global arrow_R 
    for arrow_R in player_arrows_R[:]:  # Iterate over a copy of the list
        if action == 6 or action == 10 or arrow_R.x > player.x:
            arrow_R.x += ARROW_SPEED
            if enemy1.colliderect(arrow_R):
                pygame.event.post(pygame.event.Event(ENEMY_HIT1))
                try:
                    player_arrows_R.remove(arrow_R)
                except ValueError:
                    pass
            elif enemy2.colliderect(arrow_R):
                pygame.event.post(pygame.event.Event(ENEMY_HIT2))
                try:
                    player_arrows_R.remove(arrow_R)
                except ValueError:
                    pass
            elif enemy3.colliderect(arrow_R):
                pygame.event.post(pygame.event.Event(ENEMY_HIT3))
                try:
                    player_arrows_R.remove(arrow_R)
                except ValueError:
                    pass
            elif arrow_R.x > player.x + 700 or arrow_R.x < player.x - 700:
                try:
                    player_arrows_R.remove(arrow_R)
                except ValueError:
                    pass
        else:
            try:
                player_arrows_R.remove(arrow_R)
            except ValueError:
                pass

def handle_arrows_L(player_arrows_L, action):
    global arrow_L
    for arrow_L in player_arrows_L[:]:
        if action == 5 or action == 9 or arrow_L.x < player.x:
            arrow_L.x -= ARROW_SPEED
            try:
                if enemy1.colliderect(arrow_L):
                    pygame.event.post(pygame.event.Event(ENEMY_HIT1))
                    player_arrows_L.remove(arrow_L)
                elif enemy2.colliderect(arrow_L):
                    pygame.event.post(pygame.event.Event(ENEMY_HIT2))
                    player_arrows_L.remove(arrow_L)
                elif enemy3.colliderect(arrow_L):
                    pygame.event.post(pygame.event.Event(ENEMY_HIT3))
                    player_arrows_L.remove(arrow_L)
                elif arrow_L.x > player.x + 700 or arrow_L.x < player.x - 700:
                    player_arrows_L.remove(arrow_L)
            except ValueError:
                pass
        else:
            try:
                player_arrows_L.remove(arrow_L)
            except ValueError:
                pass

def handle_arrows_UP(player_arrows_UP, action):
    global arrow_UP
    for arrow_UP in player_arrows_UP[:]:
        if action == 7 or action == 11 or arrow_UP.y < player.y:
            arrow_UP.y -= ARROW_SPEED
            try:
                if enemy1.colliderect(arrow_UP):
                    pygame.event.post(pygame.event.Event(ENEMY_HIT1))
                    player_arrows_UP.remove(arrow_UP)
                elif enemy2.colliderect(arrow_UP):
                    pygame.event.post(pygame.event.Event(ENEMY_HIT2))
                    player_arrows_UP.remove(arrow_UP)
                elif enemy3.colliderect(arrow_UP):
                    pygame.event.post(pygame.event.Event(ENEMY_HIT3))
                    player_arrows_UP.remove(arrow_UP)
                elif arrow_UP.y > player.y + 700 or arrow_UP.y < player.y - 700:
                    player_arrows_UP.remove(arrow_UP)
            except ValueError:
                pass
        else:
            try:
                player_arrows_UP.remove(arrow_UP)
            except ValueError:
                pass

def handle_arrows_DOWN(player_arrows_DOWN, action):
    global arrow_DOWN
    for arrow_DOWN in player_arrows_DOWN[:]:
        if action == 4 or action == 8 or arrow_DOWN.y > player.y + 40:
            arrow_DOWN.y += ARROW_SPEED
            try:
                if enemy1.colliderect(arrow_DOWN):
                    pygame.event.post(pygame.event.Event(ENEMY_HIT1))
                    player_arrows_DOWN.remove(arrow_DOWN)
                elif enemy2.colliderect(arrow_DOWN):
                    pygame.event.post(pygame.event.Event(ENEMY_HIT2))
                    player_arrows_DOWN.remove(arrow_DOWN)
                elif enemy3.colliderect(arrow_DOWN):
                    pygame.event.post(pygame.event.Event(ENEMY_HIT3))
                    player_arrows_DOWN.remove(arrow_DOWN)
                elif arrow_DOWN.y > player.y + 700 or arrow_DOWN.y < player.y - 700:
                    player_arrows_DOWN.remove(arrow_DOWN)
            except ValueError:
                pass
        else:
            try:
                player_arrows_DOWN.remove(arrow_DOWN)
            except ValueError:
                pass

def handle_arrows_all(player_arrows_R, player_arrows_L, player_arrows_UP, action):
    handle_arrows_R(player_arrows_R, action)
    handle_arrows_L(player_arrows_L, action)
    handle_arrows_UP(player_arrows_UP, action)
    handle_arrows_DOWN(player_arrows_DOWN, action)

class HealthBar():
    def __init__(self, x, y, w, h, max_hp):
        self.x = x 
        self.y = y
        self.w = w 
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
    def draw(self, surface):
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, RED, (WIDTH/2 - 23, HEIGHT/2 - 60, 50, 10))
        pygame.draw.rect(screen, GREEN, (WIDTH/2 - 23, HEIGHT/2 - 60, 50 * ratio, 10))
    
def main_loop():
    """
    Runs the main game loop and processes game events.
    The loop continues until the global variable `running` becomes False, and then quits the game.
    """
    global running,player_health, player, health_bar, enemy1_health, enemy2_health, enemy3_health, score, player_arrows_R, player_arrows_L, player_arrows_UP, player_arrows_DOWN, enemy1, enemy2, enemy3, current_time, dead, frame, action
    global health_pickups

    health_pickups = []

    player = pygame.Rect(icon_x, icon_y, PLAYER_WIDTH/3,PLAYER_HEIGHT/2)
    health_bar = HealthBar(250, 250, 300, 40, 100)
    player_arrows_R = []
    player_arrows_L = []
    player_arrows_UP = []
    player_arrows_DOWN = []
    player_health = 100

    
    enemy1_coordinate = enemy_spawn(player)
    enemy1_icon_x = enemy1_coordinate[0]
    enemy1_icon_y = enemy1_coordinate[1]
    enemy1_health = 50

    enemy2_coordinate = enemy_spawn(player)
    enemy2_icon_x = enemy2_coordinate[0]
    enemy2_icon_y = enemy2_coordinate[1]
    enemy2_health = 50

    enemy3_coordinate = enemy_spawn(player)
    enemy3_icon_x = enemy3_coordinate[0]
    enemy3_icon_y = enemy3_coordinate[1]
    enemy3_health = 50

    score = 0

    dead = False

    enemy1 = pygame.Rect(enemy1_icon_x, enemy1_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)
    enemy2 = pygame.Rect(enemy2_icon_x, enemy2_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)
    enemy3 = pygame.Rect(enemy3_icon_x, enemy3_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)

    while running:
        current_time = pygame.time.get_ticks()
        if enemy1_health <= 0:
            if score % 5 == 0:
                generate_health_pickup(enemy1.x, enemy1.y)
            score += 1
            enemy1_coordinate = enemy_spawn(player)
            enemy1_icon_x = enemy1_coordinate[0]
            enemy1_icon_y = enemy1_coordinate[1]
            enemy1_health = 50
            enemy1 = pygame.Rect(enemy1_icon_x, enemy1_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)
        if enemy2_health <= 0:
            if score % 5 == 0:
                generate_health_pickup(enemy2.x, enemy2.y)
            score +=1
            enemy2_coordinate = enemy_spawn(player)
            enemy2_icon_x = enemy2_coordinate[0]
            enemy2_icon_y = enemy2_coordinate[1]
            enemy2_health = 50
            enemy2 = pygame.Rect(enemy2_icon_x, enemy2_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)
        if enemy3_health <= 0:
            if score % 5 == 0:
                generate_health_pickup(enemy3.x, enemy3.y)
            score +=1
            enemy3_coordinate = enemy_spawn(player)
            enemy3_icon_x = enemy3_coordinate[0]
            enemy3_icon_y = enemy3_coordinate[1]
            enemy3_health = 50
            enemy3 = pygame.Rect(enemy3_icon_x, enemy3_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)

        # death animation execution
        if frame == 6 and action == 12:
            print("Game over")
            game_over_screen()
            break

            

        health_bar.hp = player_health
        handle_events()
        handle_arrows_all(player_arrows_R, player_arrows_L, player_arrows_UP, action)
        player_damage(player, enemy1, enemy2, enemy3)
        enemy_damage(player, enemy1, enemy2, enemy3)
        update_animation()
        update_enemy_animation()
        move_icon()
        enemy_pathfinding(enemy1, player)
        enemy_pathfinding(enemy2, player)
        enemy_pathfinding(enemy3, player)
        handle_health_pickups()
        calculate_camera_offset()
        draw_elements(enemy1, enemy2, enemy3, animation_list1, animation_list2, animation_list3, player_arrows_R, player_arrows_L, player_arrows_UP, player_arrows_DOWN)
        draw_fps_counter()

        if player_health<100:
            player_health += 0.1
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    exit()

def start_game():
    """
    Starts the main game initialization.
    """
    initialize_game()
    main_loop()

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    start_game()
