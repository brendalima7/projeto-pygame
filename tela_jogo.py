import pygame
from sprites import Jogador
from cameras import CameraGroup
import constantes

class TelaJogo:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets 

    def draw(self):
        self.window.fill(constantes.PRETO)

    def update(self):
        # tratamento de eventos - apenas transicoes de tela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'SAIR'
            
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                    return 'SAIR'
                if keys[pygame.K_a]:
                    return 'GAMEOVER' 
                if keys[pygame.K_v]:
                    return 'VITORIA' 
                    
        return 'JOGO'