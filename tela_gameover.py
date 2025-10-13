import pygame

class TelaGameOver:
    def __init__(self,window):
        self.window = window
        
    def draw(self):
        self.window.fill((100, 0, 0))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'SAIR'
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                    return 'SAIR'       
        return 'GAMEOVER'