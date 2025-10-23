"""
Módulo que define o grupo de câmera com rolagem suave (smooth camera)
e efeito de parallax para o jogo SWITCH BACK.
"""

import pygame
from constantes import *


class CameraGroup(pygame.sprite.Group):
    """Gerencia a câmera do jogo, controlando o deslocamento da visão do jogador.

    Esta classe estende `pygame.sprite.Group` e adiciona:
        - Seguimento suave do jogador (smooth follow)
        - Limitação da área visível ao tamanho do mundo
        - Efeito de parallax para o fundo
        - Desenho de sprites com base no deslocamento da câmera

    Attributes:
        display_surface (pygame.Surface): Superfície principal de exibição do jogo.
        mundo_w (int): Largura total do mundo (mapa).
        mundo_h (int): Altura total do mundo (mapa).
        offset (pygame.math.Vector2): Vetor de deslocamento atual da câmera.
        metade_w (int): Metade da largura da tela.
        metade_h (int): Metade da altura da tela.
        smooth_factor (float): Fator de suavização da movimentação da câmera.
        parallax_factor (float): Fator de deslocamento aplicado ao fundo (parallax).
    """

    def __init__(self, mundo_w, mundo_h): 
        """Inicializa o grupo de câmera com dimensões do mundo.

        Args:
            mundo_w (int): Largura total do mundo (em pixels).
            mundo_h (int): Altura total do mundo (em pixels).
        """
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.mundo_w = mundo_w
        self.mundo_h = mundo_h

        self.offset = pygame.math.Vector2()
        
        self.metade_w = self.display_surface.get_size()[0] // 2
        self.metade_h = self.display_surface.get_size()[1] // 2
        
        # Fator de suavização da câmera (0 = instantâneo, 1 = muito lento)
        self.smooth_factor = 0.05 

        # Fator de parallax para o fundo
        self.parallax_factor = 0.3

    def center_alvo_camera(self, alvo):
        """Centraliza suavemente a câmera no alvo (ex: jogador).

        Calcula o deslocamento ideal e ajusta o offset com suavização.
        Também aplica restrições para impedir que a câmera saia dos limites do mapa.

        Args:
            alvo (pygame.sprite.Sprite): Sprite cujo `rect.center` será o ponto focal da câmera.
        """
        # Posições desejadas para centralizar o alvo na tela
        desejado_x = alvo.rect.centerx - self.metade_w
        desejado_y = alvo.rect.centery - self.metade_h
        
        # Suavização do movimento (interpolação)
        self.offset.x += (desejado_x - self.offset.x) * self.smooth_factor
        self.offset.y += (desejado_y - self.offset.y) * self.smooth_factor
        
        # Limita a câmera aos limites do mapa
        if self.offset.x < 0:
            self.offset.x = 0
        if self.offset.x > self.mundo_w - WINDOWWIDHT:
            self.offset.x = self.mundo_w - WINDOWWIDHT
            
        if self.offset.y < 0:
            self.offset.y = 0
        if self.offset.y > self.mundo_h - WINDOWHEIGHT:
            self.offset.y = self.mundo_h - WINDOWHEIGHT

    def custom_draw(self, jogador, surface_fundo=None):
        """Desenha o cenário e todos os sprites com deslocamento da câmera.

        Primeiro centraliza a câmera no jogador, depois desenha o fundo
        com efeito de parallax (se fornecido) e por fim todos os sprites
        do grupo, ordenados pela posição vertical (`rect.centery`).

        Args:
            jogador (pygame.sprite.Sprite): Sprite do jogador usado como referência de câmera.
            surface_fundo (pygame.Surface, optional): Imagem de fundo para aplicar o efeito de parallax.
        """
        self.center_alvo_camera(jogador) 
    
        # Converte offset para inteiro para evitar falhas de arredondamento
        offset_int = (int(self.offset.x), int(self.offset.y))
        
        # Fundo com parallax
        if surface_fundo:
            parallax_offset_x = self.offset.x * self.parallax_factor
            parallax_offset_y = self.offset.y * self.parallax_factor
        
            self.display_surface.blit(
                surface_fundo, 
                (-parallax_offset_x, -parallax_offset_y)
            )

        # Desenha os sprites ordenados por profundidade (centro Y)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            # Posição final do sprite (posição global - offset da câmera)
            offset_pos = sprite.rect.topleft - pygame.math.Vector2(offset_int)
            self.display_surface.blit(sprite.image, offset_pos)
            
    def get_offset_pos(self, pos_x, pos_y):
        """Retorna uma posição ajustada pelo deslocamento atual da câmera.

        Args:
            pos_x (int): Coordenada X original.
            pos_y (int): Coordenada Y original.

        Returns:
            tuple[int, int]: Coordenadas ajustadas de acordo com o offset atual.
        """
        return pos_x - int(self.offset.x), pos_y - int(self.offset.y)
    
    def draw_mapa_sem_parallax(self, jogador, map_surface):
        """Desenha o mapa e os sprites sem aplicar o efeito de parallax.

        Útil para camadas do mundo que devem acompanhar a câmera rigidamente
        (ex: o chão ou o mapa base).

        Args:
            jogador (pygame.sprite.Sprite): Sprite usado para centralizar a câmera.
            map_surface (pygame.Surface): Imagem do mapa a ser desenhada.
        """
        # Calcula o offset normal
        self.center_alvo_camera(jogador) 
        offset_int = (int(self.offset.x), int(self.offset.y))
        
        # Desenha o mapa com rolagem padrão
        self.display_surface.blit(map_surface, (-offset_int[0], -offset_int[1]))

        # Desenha os sprites com offset
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - pygame.math.Vector2(offset_int)
            self.display_surface.blit(sprite.image, offset_pos)
