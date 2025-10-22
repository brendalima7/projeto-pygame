import pygame
import math

class TelaGameOver:
    def __init__(self, window, assets, fade_period=2.5, parallax_amp=6):
        self.window = window
        self.assets = assets
        self.img1 = assets['game_over1']
        self.img2 = assets['game_over2']
        self.w, self.h = self.window.get_size()

        # parâmetros de animação
        self.time = 0.0
        self.fade_period = fade_period

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                return 'SAIR'
            if event.key == pygame.K_SPACE:
                return 'RESTART'
        return None

    def update(self, dt):
        self.time += dt
        return 'GAMEOVER'

    def draw(self):
        w, h = self.w, self.h
        screen = self.window

        phase = (2 * math.pi * (self.time / self.fade_period))
        alpha = (math.sin(phase) + 1.0) / 4.0

        a1 = int((1.0 - alpha) * 255)
        a2 = int(alpha * 255)

        # cria cópias para aplicar alpha
        img1 = self.img1.copy()
        img2 = self.img2.copy()
        img1.set_alpha(a1)
        img2.set_alpha(a2)

        # centraliza as imagens
        rect1 = img1.get_rect(center=(w//2, h//2))
        rect2 = img2.get_rect(center=(w//2, h//2))

        # desenha (uma sobre a outra)
        screen.blit(img1, rect1)
        screen.blit(img2, rect2)
   
        txt = self.assets['fonte2'].render("Pressione SPACE para reiniciar", True, (255,255,255))
        screen.blit(txt, (w//2 - txt.get_width()//2, h - 100))
