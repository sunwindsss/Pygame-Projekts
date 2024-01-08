import pygame
import sys
import entry  # Game code module
import time  # For delay

def main_menu():
    pygame.init()
    WIDTH, HEIGHT = 1000, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("IKONIKS")

    # Load images
    mainmenu = pygame.image.load('images/mainmenu.png')
    titlecard = pygame.image.load('images/titlecard.png')
    start_buttons = [pygame.image.load(f'images/start-{i}.png') for i in range(1, 4)]
    info_buttons = [pygame.image.load(f'images/info-{i}.png') for i in range(1, 4)]
    credits_buttons = [pygame.image.load(f'images/credits-{i}.png') for i in range(1, 4)]
    quit_buttons = [pygame.image.load(f'images/quit-{i}.png') for i in range(1, 4)]
    close_buttons = [pygame.image.load(f'images/close-{i}.png') for i in range(1, 4)]  # Close button variations
    info_bg = pygame.image.load('images/info-bg.png')
    credits_bg = pygame.image.load('images/credits-bg.png')

    # Rectangles for buttons and images
    titlecard_rect = titlecard.get_rect(center=(WIDTH / 2, HEIGHT / 4))
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
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button_name, rect in button_rects.items():
                    if rect.collidepoint(mouse_pos):
                        current_button_images[button_name] = 2  # Set to 'click' image
                        screen.blit(mainmenu, (0, 0))
                        if not (show_info or show_credits):  # Only display titlecard when main menu is visible
                            screen.blit(titlecard, titlecard_rect)
                        draw_buttons(screen, current_button_images, start_buttons, info_buttons, credits_buttons, quit_buttons, close_buttons, button_rects)
                        pygame.display.update()
                        time.sleep(0.1)  # 100ms delay
                        if button_name == "start" and not (show_info or show_credits):
                            running = False
                            entry.start_game()  # Start the game from entry.py
                        elif button_name == "info":
                            show_info = True
                        elif button_name == "credits":
                            show_credits = True
                        elif button_name == "close" and (show_info or show_credits):
                            show_info = False
                            show_credits = False
                        elif button_name == "quit" and not (show_info or show_credits):
                            pygame.quit()
                            sys.exit()
                        current_button_images[button_name] = 0  # Reset to 'normal' image

        # Update button images based on hover
        for button_name, rect in button_rects.items():
            if rect.collidepoint(mouse_pos):
                current_button_images[button_name] = 1  # Set to 'hover' image
            else:
                current_button_images[button_name] = 0  # Reset to 'normal' image

        screen.blit(mainmenu, (0, 0))
        if not (show_info or show_credits):  # Only display titlecard when main menu is visible
            screen.blit(titlecard, titlecard_rect)
        draw_buttons(screen, current_button_images, start_buttons, info_buttons, credits_buttons, quit_buttons, close_buttons, button_rects)

        if show_info:
            screen.blit(info_bg, (0, 0))
            screen.blit(close_buttons[current_button_images["close"]], button_rects["close"])  # Use current close button image
        elif show_credits:
            screen.blit(credits_bg, (0, 0))
            screen.blit(close_buttons[current_button_images["close"]], button_rects["close"])  # Use current close button image

        pygame.display.update()

def draw_buttons(screen, current_button_images, start_buttons, info_buttons, credits_buttons, quit_buttons, close_buttons, button_rects):
    screen.blit(start_buttons[current_button_images["start"]], button_rects["start"])
    screen.blit(info_buttons[current_button_images["info"]], button_rects["info"])
    screen.blit(credits_buttons[current_button_images["credits"]], button_rects["credits"])
    screen.blit(quit_buttons[current_button_images["quit"]], button_rects["quit"])
    if current_button_images["close"] != 0 and current_button_images["close"] != 1 and current_button_images["close"] != 2:  # Draw close button only if it's not in the normal state
        screen.blit(close_buttons[current_button_images["close"]], button_rects["close"])

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    main_menu()
