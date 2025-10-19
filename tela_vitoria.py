import pygame

class TelaVitoria:
    def __init__(self,window):
        self.window = window
        
    def draw(self):
        self.window.fill((0, 200, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return 'SAIR'
            # if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
            #     return 'JOGO'  # pode ir direto pro jogo também
        return None

    def update(self, dt):
       
        return 'VITORIA'