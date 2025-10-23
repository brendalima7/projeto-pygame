import pygame
import math

class TelaGameOver:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets
        

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                return 'SAIR'
            if event.key == pygame.K_SPACE:
                return 'RESTART'
            if event.key == pygame.K_r:
                return 'RANKING'
        return None

    def update(self, dt):
        return 'GAMEOVER'

    def draw(self):
        self.window.fill((0,100,100))
        self.window.blit(self.assets['game_over'],(0,0))
        
        txt = self.assets['fonte2'].render("PRESSIONE SPACE PARA RECOMEÇAR", True, (255, 255, 255))
    
        pos_x_txt = self.window.get_width() // 2 - txt.get_width() // 2

        rank = self.assets['fonte2'].render("PRESSIONE R PARA VER RANKING", True, (255, 255, 255))
    
        pos_x_rank = self.window.get_width() // 2 - rank.get_width() // 2

        
        self.window.blit(txt, (pos_x_txt,750))
        self.window.blit(rank, (pos_x_rank,800))
