import pygame
from constantes import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self, mundo_w, mundo_h): 
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.mundo_w = mundo_w
        self.mundo_h = mundo_h

        self.offset = pygame.math.Vector2()
        
        self.metade_w = self.display_surface.get_size()[0] // 2
        self.metade_h = self.display_surface.get_size()[1] // 2
        
        # smooth factor -  controle de velocidade do seguimento.
        self.smooth_factor = 0.05 

        self.parallax_factor = 0.3

    def center_alvo_camera(self, alvo):
        # posicoes desejadas - para onde o centro da tela deveria ir 
        desejado_x = alvo.rect.centerx - self.metade_w
        desejado_y = alvo.rect.centery - self.metade_h
        
        # smooth follow 
        self.offset.x += (desejado_x - self.offset.x) * self.smooth_factor
        self.offset.y += (desejado_y - self.offset.y) * self.smooth_factor
        
        # limitacao da camera - impede que a camera saia do mapa
        if self.offset.x < 0:
            self.offset.x = 0
        if self.offset.x > self.mundo_w - WINDOWWIDHT:
            self.offset.x = self.mundo_w - WINDOWWIDHT
            
        if self.offset.y < 0:
            self.offset.y = 0
        if self.offset.y > self.mundo_h - WINDOWHEIGHT:
            self.offset.y = self.mundo_h - WINDOWHEIGHT

    
    def custom_draw(self, jogador, surface_fundo=None):

        self.center_alvo_camera(jogador) 
    
        # conversao de offset para evitar falhas de desenho
        offset_int = (int(self.offset.x), int(self.offset.y))
        
        # background
        if surface_fundo:
            parallax_offset_x = self.offset.x * self.parallax_factor
            parallax_offset_y = self.offset.y * self.parallax_factor
        
            self.display_surface.blit(
                surface_fundo, 
                (-parallax_offset_x, -parallax_offset_y)
            )

        # desenhando sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # calcula a posicao final do sprite na tela (posicao no mundo - offset da camera)
            offset_pos = sprite.rect.topleft - pygame.math.Vector2(offset_int)
            self.display_surface.blit(sprite.image, offset_pos)
            
    def get_offset_pos(self, pos_x, pos_y):
        return pos_x - int(self.offset.x), pos_y - int(self.offset.y)
    
    def draw_mapa_sem_parallax(self, jogador, map_surface):
        # Calcula o offset normal
        self.center_alvo_camera(jogador) 
        offset_int = (int(self.offset.x), int(self.offset.y))
        
        # desenha o mapa - rolagem padrao
        self.display_surface.blit(map_surface, (-offset_int[0], -offset_int[1]))

        # desenha os sprites com offset
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - pygame.math.Vector2(offset_int)
            self.display_surface.blit(sprite.image, offset_pos)