import pygame
import spritesheet
import random

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
    global background_image, sprite_sheet, black_background, enemy_sprite_sheet1, enemy_sprite_sheet2
    background_image = pygame.image.load('images/grass_bg.png')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    sprite_sheet_image = pygame.image.load('images/player.png').convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

    enemy_sprite_sheet_image1 = pygame.image.load('images/enemy1.png').convert_alpha()
    enemy_sprite_sheet1 = spritesheet.SpriteSheet(enemy_sprite_sheet_image1)

    enemy_sprite_sheet_image2 = pygame.image.load('images/doux_upgrade.png').convert_alpha()
    enemy_sprite_sheet2 = spritesheet.SpriteSheet(enemy_sprite_sheet_image2)

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

def create_enemy_animation_list(enemy_sprite_sheet):
    global enemy_animation_list, enemy_action, enemy_frame, enemy_step_counter, enemy_last_update, enemy_animation_cooldown
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
    
    return enemy_animation_list

def initialize_game():
    global animation_list1, animation_list2
    pygame.init()
    set_static_variables()
    set_color_codes()
    set_basic_settings()
    load_images()
    create_animation_list()
    animation_list1 = create_enemy_animation_list(enemy_sprite_sheet1)
    animation_list2 = create_enemy_animation_list(enemy_sprite_sheet2)

PLAYER_HIT = pygame.USEREVENT + 1
ENEMY_HIT1 = pygame.USEREVENT + 2
ENEMY_HIT2 = pygame.USEREVENT + 3
def handle_events():
    global running, last_lift_up, player_health, enemy1_health, enemy2_health
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            last_lift_up = event.key
        elif event.type == PLAYER_HIT:
            player_health -= 1
        elif event.type == ENEMY_HIT1:
            enemy1_health -= 1
        elif event.type == ENEMY_HIT2:
            enemy2_health -= 1
            


def update_animation():
    global frame, last_update, animation_cooldown, action

    # Update player animations
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0
            
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
    global player, action
    keys = pygame.key.get_pressed()

    # Adjust speed based on linear or diagonal movement
    if (keys[pygame.K_w] or keys[pygame.K_s]) and (keys[pygame.K_a] or keys[pygame.K_d]):
        speed = speed_diagonal  # Reduce speed for diagonal movement
    else:
        speed = speed_linear  # Reset speed for non-diagonal movement

    if keys[pygame.K_s] and player.y < HEIGHT - PLAYER_HEIGHT:
        player.y += speed
        action = 0
    if keys[pygame.K_d] and player.x < WIDTH - PLAYER_WIDTH:
        player.x += speed
        action = 2
    if keys[pygame.K_a] and player.x > 0:
        player.x -= speed
        action = 1
    if keys[pygame.K_w] and player.y > 0:
        player.y -= speed
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
        enemy_action = 1
    if player.x < enemy.x:
        enemy.x -= speed/2
        enemy_action = 3
    if player.y > enemy.y:
        enemy.y += speed/2
    if player.y < enemy.y:
        enemy.y -= speed/2

def enemy_spawn():
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

def calculate_camera_offset():
    global camera_x, camera_y
    camera_x = player.x - (WIDTH / 2) + (PLAYER_WIDTH / 2)
    camera_y = player.y - (HEIGHT / 2) + (PLAYER_HEIGHT / 2)

def draw_elements(enemy1, enemy2, enemy_animation_list1, enemy_animation_list2):
    screen.blit(black_background, (camera_x - (BACKGROUND_WIDTH / 2), camera_y - (BACKGROUND_HEIGHT / 2)))
    screen.blit(background_image, (-camera_x, -camera_y))
    screen.blit(enemy_animation_list1[enemy_action][enemy_frame], (enemy1.x - camera_x + 28, enemy1.y - camera_y + 28))
    screen.blit(enemy_animation_list2[enemy_action][enemy_frame], (enemy2.x - camera_x + 28, enemy2.y - camera_y + 28))
    screen.blit(animation_list[action][frame], (player.x - camera_x, player.y - camera_y))
    health_bar.draw(screen)

def draw_fps_counter():
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (10, 10))

def player_damage(player, enemy1, enemy2):
    if player.colliderect(enemy1):
        pygame.event.post(pygame.event.Event(PLAYER_HIT))
    if player.colliderect(enemy2):
        pygame.event.post(pygame.event.Event(PLAYER_HIT))

def enemy_damage(player, enemy1, enemy2):
    if player.colliderect(enemy1):
        pygame.event.post(pygame.event.Event(ENEMY_HIT1))
    if player.colliderect(enemy2):
        pygame.event.post(pygame.event.Event(ENEMY_HIT2))
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
    global running,player_health, player, health_bar, enemy1_health, enemy2_health

    enemy1_coordinate = enemy_spawn()
    enemy1_icon_x = enemy1_coordinate[0]
    enemy1_icon_y = enemy1_coordinate[1]
    enemy1_health = 50
    enemy1_count = 0

    enemy2_coordinate = enemy_spawn()
    enemy2_icon_x = enemy2_coordinate[0]
    enemy2_icon_y = enemy2_coordinate[1]
    enemy2_health = 50
    enemy2_count = 0

    player = pygame.Rect(icon_x, icon_y, PLAYER_WIDTH/3,PLAYER_HEIGHT/2)
    health_bar = HealthBar(250, 250, 300, 40, 100)
    player_health = 100

    
    enemy1 = pygame.Rect(enemy1_icon_x, enemy1_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)
    enemy2 = pygame.Rect(enemy2_icon_x, enemy2_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)

    while running:
        if enemy1_health == 0:
            enemy1_count += 1
            enemy1_coordinate = enemy_spawn()
            enemy1_icon_x = enemy1_coordinate[0]
            enemy1_icon_y = enemy1_coordinate[1]
            enemy1_health = 50
            enemy1 = pygame.Rect(enemy1_icon_x, enemy1_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)
            print(enemy1_count)
        if enemy2_health == 0:
            enemy2_count +=1
            enemy2_coordinate = enemy_spawn()
            enemy2_icon_x = enemy2_coordinate[0]
            enemy2_icon_y = enemy2_coordinate[1]
            enemy2_health = 50
            enemy2 = pygame.Rect(enemy2_icon_x, enemy2_icon_y, PLAYER_WIDTH/2,PLAYER_HEIGHT/2)
            print(enemy2_count)
        handle_events()
        health_bar.hp = player_health
        player_damage(player, enemy1, enemy2)
        enemy_damage(player, enemy1, enemy2)
        update_animation()
        update_enemy_animation()
        move_icon()
        enemy_pathfinding(enemy1, player)
        enemy_pathfinding(enemy2, player)
        calculate_camera_offset()
        draw_elements(enemy1, enemy2, animation_list1, animation_list2)
        draw_fps_counter()
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    initialize_game()
    main_loop()
