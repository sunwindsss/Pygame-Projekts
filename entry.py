import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600)) # flags=pygame.NOFRAME
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

running = True

while running:

    # screen.fill((252, 186, 3))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                screen.fill((3, 24, 252))
                pygame.display.update()