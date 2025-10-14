# ARQUIVO: scrollingcamera.py

import pygame
import constantes # Importar constantes para usar as dimensões do mundo

class CameraGroup(pygame.sprite.Group):
    # Recebe as dimensões do mundo para limitar o scrolling
    def __init__(self, mundo_w, mundo_h): 
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Dimensões do mundo
        self.mundo_w = mundo_w
        self.mundo_h = mundo_h

        # Variável para armazenar o deslocamento da câmera
        self.offset = pygame.math.Vector2()
        
        # Metade da largura/altura da TELA (para centralizar o jogador)
        self.metade_w = self.display_surface.get_size()[0] // 2
        self.metade_y = self.display_surface.get_size()[1] // 2

        # Removido ground_surface e ground_rect fixos daqui (será gerenciado pelas Telas)

    def center_alvo_camera(self, alvo):
        # 1. Calcular o deslocamento padrão (centralizar o alvo)
        self.offset.x = alvo.rect.centerx - self.metade_w
        self.offset.y = alvo.rect.centery - self.metade_y
        
        # 2. LIMITAÇÃO DA CÂMERA (Impede a câmera de sair do mapa)
        
        # Limite X: O offset (canto superior esquerdo da tela no mundo) não pode ser
        # menor que 0 ou maior que (Largura do Mundo - Largura da Tela)
        if self.offset.x < 0:
            self.offset.x = 0
        if self.offset.x > self.mundo_w - constantes.WINDOWWIDHT:
            self.offset.x = self.mundo_w - constantes.WINDOWWIDHT
            
        # Limite Y
        if self.offset.y < 0:
            self.offset.y = 0
        if self.offset.y > self.mundo_h - constantes.WINDOWHEIGHT:
            self.offset.y = self.mundo_h - constantes.WINDOWHEIGHT

    def custom_draw(self, jogador, surface_fundo=None):
        self.center_alvo_camera(jogador)

        # 1. Desenho do Fundo (se fornecido)
        # O fundo é desenhado no canto superior esquerdo da TELA, mas deslocado pelo offset
        if surface_fundo:
             # O sinal de menos (-) é crucial aqui para mover o fundo na direção oposta ao offset
            self.display_surface.blit(surface_fundo, -self.offset)

        # 2. Desenho dos Sprites
        # Usamos o sort() para desenhar sprites mais baixos por último (cria efeito 3D/profundidade)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # Calcula a posição final do sprite na tela (posição no mundo - offset da câmera)
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)