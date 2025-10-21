import pygame

class TelaGameOver:
    def __init__(self, window):
        self.window = window
    def draw(self):
        self.window.fill((100, 0, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return 'SAIR'
            # if event.key == pygame.K_r:
            #     return 'RESTART'
            if event.key == pygame.K_SPACE:
                return 'RESTART'
        return None

    def update(self, dt):
        # não há lógica dinâmica necessária aqui; apenas mantém a assinatura
        return 'GAMEOVER'
