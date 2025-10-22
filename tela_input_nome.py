import pygame
from constantes import * # Importa WINDOWWIDHT, WINDOWHEIGHT, etc.

# --- Cores e InputBox (Componente para entrada de texto) ---
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('white')

class InputBox:
    def __init__(self, x, y, w, h, font, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_ACTIVE
        self.text = text
        self.font = font
        self.active = True
        self.txt_surface = font.render(text, True, COLOR_TEXT)
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = 10 

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text.strip(): # Só permite continuar se o nome não for vazio
                        return 'COMPLETO', self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_length:
                    if event.unicode.isalnum() or event.unicode.isspace():
                        self.text += event.unicode.upper() 
                
                self.txt_surface = self.font.render(self.text, True, COLOR_TEXT)
                self.cursor_timer = 0 
        
        return None, None 

    def update(self, dt):
        self.cursor_timer += 1
        if self.cursor_timer > 30: 
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 3) 
        
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + self.txt_surface.get_width()
            cursor_y = self.rect.y + 5
            cursor_h = self.rect.h - 10 
            pygame.draw.line(screen, COLOR_TEXT, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_h), 2)


# --- Tela principal ---
class TelaInputNome:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets

        largura = 350
        altura = 60
        x = (WINDOWWIDHT // 2) - (largura // 2)
        y = (WINDOWHEIGHT // 2)
        
        self.input_box = InputBox(x, y, largura, altura, self.assets['fonte2'])

    def handle_event(self, event):
        retorno, nome_digitado = self.input_box.handle_event(event)
        
        if retorno == 'COMPLETO':
            # Retorna o próximo estado ('INICIO') E o nome capturado
            return 'INICIO', nome_digitado.strip()
            
        return None

    def update(self, dt):
        self.input_box.update(dt)
        return 'INPUT_NOME'

    def draw(self):
        self.window.fill((0, 0, 0))
        
        titulo = self.assets['fonte'].render("SWITCH BACK", True, (255, 255, 255))
        instrucao = self.assets['fonte2'].render("DIGITE SEU NOME (ENTER):", True, (200, 200, 200))
        
        rect_titulo = titulo.get_rect(center=(WINDOWWIDHT // 2, WINDOWHEIGHT // 2 - 150))
        self.window.blit(titulo, rect_titulo)

        rect_instrucao = instrucao.get_rect(center=(WINDOWWIDHT // 2, self.input_box.rect.y - 40))
        self.window.blit(instrucao, rect_instrucao)
        
        self.input_box.draw(self.window)