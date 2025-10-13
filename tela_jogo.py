import pygame
from sprites import Jogador

# elementos jogaveis e logica de interacao
class TelaJogo:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets  
        self.jogador = Jogador(self.window, self.assets)  

    def draw(self):
        self.window.fill((0, 0, 0))
        self.jogador.draw() 

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'SAIR'
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                    return 'SAIR'       
        return True