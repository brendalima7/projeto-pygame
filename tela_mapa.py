import pygame

class TelaMapa:

    def __init__(self,window):
        self.window = window

    def draw(self):
        self.window.fill((255,255,255))

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'SAIR'
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                    return 'SAIR'
                if keys[pygame.K_j]:
                    return 'JOGO'  
        return 'MAPA'