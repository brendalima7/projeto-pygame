import pygame
import constantes 

class CameraGroup(pygame.sprite.Group):
    def __init__(self, mundo_w, mundo_h): 
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.mundo_w = mundo_w
        self.mundo_h = mundo_h

        self.offset = pygame.math.Vector2()
        
        self.metade_w = self.display_surface.get_size()[0] // 2
        self.metade_y = self.display_surface.get_size()[1] // 2
        
        # smooth factor -  controle de velocidade do seguimento.
        self.smooth_factor = 0.05 

    def center_alvo_camera(self, alvo):
        # posicoes desejadas - para onde o centro da tela deveria ir 
        desejado_x = alvo.rect.centerx - self.metade_w
        desejado_y = alvo.rect.centery - self.metade_y
        
        # smooth follow 
        self.offset.x += (desejado_x - self.offset.x) * self.smooth_factor
        self.offset.y += (desejado_y - self.offset.y) * self.smooth_factor
        
        # limitacao da camera - impede que a camera saia do mapa
        if self.offset.x < 0:
            self.offset.x = 0
        if self.offset.x > self.mundo_w - constantes.WINDOWWIDHT:
            self.offset.x = self.mundo_w - constantes.WINDOWWIDHT
            
        if self.offset.y < 0:
            self.offset.y = 0
        if self.offset.y > self.mundo_h - constantes.WINDOWHEIGHT:
            self.offset.y = self.mundo_h - constantes.WINDOWHEIGHT

    
    def custom_draw(self, jogador, surface_fundo=None):

        self.center_alvo_camera(jogador) 
    
        # conversao de offset para evitar falhas de desenho
        offset_int = (int(self.offset.x), int(self.offset.y))
        
        # background
        if surface_fundo:
            self.display_surface.blit(surface_fundo, -self.offset)

        # desenhando sprites
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # calcula a posicao final do sprite na tela (posicao no mundo - offset da camera)
            offset_pos = sprite.rect.topleft - pygame.math.Vector2(offset_int)
            self.display_surface.blit(sprite.image, offset_pos)
            
    def get_offset_pos(self, pos_x, pos_y):
        return pos_x - int(self.offset.x), pos_y - int(self.offset.y)