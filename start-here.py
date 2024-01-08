import pygame
import sys
import entry  # Game code module

def main_menu():
    """
    Handles main game menu functionality.
    Loads every image associated with the main menu and sets up display proportions for the buttons.
    Handles button clicks and animation events for button presses.
    """
    pygame.init()
    WIDTH, HEIGHT = 1000, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    icon = pygame.image.load('images/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption("IKONIKS")

    # Load images
    mainmenu = pygame.image.load('images/mainmenu.png')
    titlecard = pygame.image.load('images/titlecard.png')
    start_button = pygame.image.load('images/start-1.png')
    info_button = pygame.image.load('images/info-1.png')
    credits_button = pygame.image.load('images/credits-1.png')
    quit_button = pygame.image.load('images/quit-1.png')
    info_bg = pygame.image.load('images/info-bg.png')
    credits_bg = pygame.image.load('images/credits-bg.png')
    close_button = pygame.image.load('images/close-1.png')

    # Rectangles for buttons and images
    titlecard_rect = titlecard.get_rect(center=(WIDTH / 2, HEIGHT / 4))
    start_button_rect = start_button.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 25)) # Adjust height values for button gaps
    info_button_rect = info_button.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 85))
    credits_button_rect = credits_button.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 200))
    quit_button_rect = quit_button.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 315))
    close_button_rect = close_button.get_rect(center=(WIDTH / 2, HEIGHT - 100))

    running = True
    show_info = False
    show_credits = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos) and not (show_info or show_credits):
                    running = False
                    entry.start_game()  # Start the game from entry.py
                elif info_button_rect.collidepoint(event.pos):
                    show_info = True
                elif credits_button_rect.collidepoint(event.pos):
                    show_credits = True
                elif close_button_rect.collidepoint(event.pos) and (show_info or show_credits):
                    show_info = False
                    show_credits = False
                elif quit_button_rect.collidepoint(event.pos) and not (show_info or show_credits):
                    pygame.quit()
                    sys.exit()

        screen.blit(mainmenu, (0, 0))

        if show_info:
            screen.blit(info_bg, (0, 0))
            screen.blit(close_button, close_button_rect)
        elif show_credits:
            screen.blit(credits_bg, (0, 0))
            screen.blit(close_button, close_button_rect)
        else:
            screen.blit(titlecard, titlecard_rect)
            screen.blit(start_button, start_button_rect)
            screen.blit(info_button, info_button_rect)
            screen.blit(credits_button, credits_button_rect)
            screen.blit(quit_button, quit_button_rect)

        pygame.display.update()

# Check if this script is being run directly (not imported as a module)
if __name__ == "__main__":
    main_menu()
