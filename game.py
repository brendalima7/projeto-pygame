import pygame

pygame.init()

# full screen 
info = pygame.display.Info()
WINDOWWIDHT = info.current_w
WINDOWHEIGHT = info.current_h

window = pygame.display.set_mode((WINDOWWIDHT, WINDOWHEIGHT))
pygame.display.set_caption('Game')

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                game = False

    window.fill((0, 0, 0))
    pygame.display.update()