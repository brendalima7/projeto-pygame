import pygame
import math

class TelaInstrucoes2:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets    

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                return 'SAIR'
            if event.key == pygame.K_SPACE:
                return 'JOGO'
        return None

    def update(self, dt):
        return 'INSTRUCOES2'

    def draw(self):
        self.window.fill((0,100,100))
        self.window.blit(self.assets['tela_instrucoes2'],(0,0))
        
