import pygame
import entry  # Game code module

# Function to load sounds
def load_sounds():
    """
    Loads sound effects and music for the game.
    Adjusts volume settings for the sounds.
    """
    global menu_music, game_music, start_sound, infocredits_sound, backquit_sound
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init() # Initialize the pygame mixer module

    # Load sound effects
    start_sound = pygame.mixer.Sound('sounds/start.ogg')
    infocredits_sound = pygame.mixer.Sound('sounds/infocredits.ogg')
    backquit_sound = pygame.mixer.Sound('sounds/backquit.ogg')

    # Load and play background music
    menu_music = pygame.mixer.Sound('sounds/menu-music.mp3')
    game_music = pygame.mixer.Sound('sounds/game-music.mp3')

    # Volume settings for the sounds
    start_sound.set_volume(0.1)
    infocredits_sound.set_volume(0.1)
    backquit_sound.set_volume(0.1)
    menu_music.set_volume(0.1)
    game_music.set_volume(0.1)

    menu_music.play(-1)  # The '-1' argument makes the music play indefinitely


def main_menu():
    """
    Handles main menu functionality.
    Draws button images, backgrounds, credits and control scheme screens.
    Handles button animations like hovers and presses in the main menu.
    """
    pygame.init()
    WIDTH, HEIGHT = 1000, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("IKONIKS")
    
    load_sounds()  # Load sounds and start playing menu music

    # Load images
    mainmenu = pygame.image.load('images/mainmenu.png')
    start_buttons = [pygame.image.load(f'images/start-{i}.png') for i in range(1, 4)]
    info_buttons = [pygame.image.load(f'images/info-{i}.png') for i in range(1, 4)]
    credits_buttons = [pygame.image.load(f'images/credits-{i}.png') for i in range(1, 4)]
    quit_buttons = [pygame.image.load(f'images/quit-{i}.png') for i in range(1, 4)]
    close_buttons = [pygame.image.load(f'images/close-{i}.png') for i in range(1, 4)]  # Close button variations
    info_bg = pygame.image.load('images/info-bg.png')
    credits_bg = pygame.image.load('images/credits-bg.png')

    # Rectangles for buttons and images
    button_rects = {
        "start": start_buttons[0].get_rect(center=(WIDTH / 2, HEIGHT / 2 - 25)),
        "info": info_buttons[0].get_rect(center=(WIDTH / 2, HEIGHT / 2 + 85)),
        "credits": credits_buttons[0].get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200)),
        "quit": quit_buttons[0].get_rect(center=(WIDTH / 2, HEIGHT / 2 + 315)),
        "close": close_buttons[0].get_rect(center=(WIDTH / 2, HEIGHT - 100))
    }

    running = True
    show_info = False
    show_credits = False
    current_button_images = {
        "start": 0,
        "info": 0,
        "credits": 0,
        "quit": 0,
        "close": 0  # Initialize state for close button
    }

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button_name, rect in button_rects.items():
                    if rect.collidepoint(mouse_pos):
                        # Update button state to 'click' (DOESN'T WORK)
                        current_button_images[button_name] = 2
                        pygame.display.update()
                        
                        # Process main menu button clicks only when neither info nor credits screen is active
                        if not (show_info or show_credits):
                            if button_name == "start":
                                start_sound.play()
                                menu_music.stop()
                                game_music.play(-1)
                                pygame.time.delay(100)
                                running = False
                                entry.start_game()
                            elif button_name == "info":
                                infocredits_sound.play()
                                pygame.time.delay(100)
                                show_info = True
                            elif button_name == "credits":
                                infocredits_sound.play()
                                pygame.time.delay(100)
                                show_credits = True
                            elif button_name == "quit":
                                backquit_sound.play()
                                pygame.time.delay(100)
                                pygame.quit()

                        # Process close button clicks only when info or credits screen is active
                        if (show_info or show_credits) and button_name == "close":
                            backquit_sound.play()
                            pygame.time.delay(100)
                            show_info = False
                            show_credits = False

        # Update button images based on hover
        for button_name, rect in button_rects.items():
            if rect.collidepoint(mouse_pos):
                current_button_images[button_name] = 1  # Set to 'hover' image
            else:
                current_button_images[button_name] = 0  # Reset to 'normal' image

        screen.blit(mainmenu, (0, 0))
        draw_buttons(screen, current_button_images, start_buttons, info_buttons, credits_buttons, quit_buttons, button_rects)

        if show_info:
            screen.blit(info_bg, (0, 0))
            screen.blit(close_buttons[current_button_images["close"]], button_rects["close"])
        elif show_credits:
            screen.blit(credits_bg, (0, 0))
            screen.blit(close_buttons[current_button_images["close"]], button_rects["close"])

        pygame.display.update()


def draw_buttons(screen, current_button_images, start_buttons, info_buttons, credits_buttons, quit_buttons, button_rects):
    """
    Handles button drawing in the main menu.
    """
    screen.blit(start_buttons[current_button_images["start"]], button_rects["start"])
    screen.blit(info_buttons[current_button_images["info"]], button_rects["info"])
    screen.blit(credits_buttons[current_button_images["credits"]], button_rects["credits"])
    screen.blit(quit_buttons[current_button_images["quit"]], button_rects["quit"])

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    main_menu()
