import pygame 

class TelaInicio:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets

        self.alpha = 0  
        self.fade_speed = 600 
        self.fade_direction = 1 
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return 'SAIR'
            if event.key == pygame.K_SPACE:
                return 'INPUT_NOME'
        return None
        
    def update(self, dt):
        self.alpha += self.fade_direction * self.fade_speed * dt 
        if self.alpha >= 255:
            self.alpha = 255
            self.fade_direction = -1 # Começa a diminuir
        elif self.alpha <= 0:
            self.alpha = 0
            self.fade_direction = 1 
        return 'INICIO'
    
    def draw(self):
        self.window.fill((0,100,100))
        self.window.blit(self.assets['fundo_inicial'],(0,0))
        img_tempo = self.assets['fonte2'].render("PRESSIONE SPACE PARA JOGAR", True, (255, 255, 255))
        img_tempo.set_alpha(int(self.alpha))
        pos_x = self.window.get_width() // 2 - img_tempo.get_width() // 2
        self.window.blit(img_tempo, (pos_x, 720))