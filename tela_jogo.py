import pygame
from sprites import Jogador # Importando a classe Jogador corrigida
from cameras import CameraGroup
import constantes

# representa um pedaço do mapa para colisão. 
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)

class TelaJogo:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets
        
        # dimensoes do mapa
        MAP_W_FASE = 5000
        MAP_H_FASE = 2500
        
        self.camera_group = CameraGroup(MAP_W_FASE, MAP_H_FASE)

        self.jogador = Jogador(self.window, self.assets)
        self.camera_group.add(self.jogador) 

        self.fundo_normal = self.assets['fundo_mundonormal']
        self.fundo_largura = self.fundo_normal.get_width() 
        self.fundo_x = 0 

        self.mapa_do_jogo = self.assets['mapa_do_jogo']

        # tamanho dos blocos (tiles)
        self.tile_size = 500
        self.tiles = self.criar_tiles_otimizado(self.mapa_do_jogo)

    def criar_tiles_otimizado(self, mapa_surface):
        tiles = []
        largura, altura = mapa_surface.get_size()

        for y in range(0, altura, self.tile_size):
            for x in range(0, largura, self.tile_size):
                # recorte da parte do mapa
                tile_surface = mapa_surface.subsurface(
                    pygame.Rect(x, y, self.tile_size, self.tile_size)
                ).copy()

                # cria uma máscara temporária
                mask_temp = pygame.mask.from_surface(tile_surface)

                # verifica se o tile tem pelo menos 1 pixel opaco
                if mask_temp.count() > 0:
                    tile = Tile(tile_surface, (x, y))
                    tiles.append(tile)
        return tiles
    
    def checar_colisao(self):
        jogador_mask = pygame.mask.from_surface(self.jogador.image)
        jogador_offset = self.jogador.rect.topleft

        colisao_detectada = False

        # área visível da câmera
        camera_rect = pygame.Rect(
            self.camera_group.offset.x,
            self.camera_group.offset.y,
            constantes.WINDOWWIDHT,
            constantes.WINDOWHEIGHT
        )

        # verifica colisão só nos tiles visíveis
        for tile in self.tiles:
            if camera_rect.colliderect(tile.rect):
                offset_x = tile.rect.x - jogador_offset[0]
                offset_y = tile.rect.y - jogador_offset[1]
                if jogador_mask.overlap(tile.mask, (offset_x, offset_y)):
                    colisao_detectada = True
                    break

        if colisao_detectada:
            # reverte o movimento pra impedir atravessar
            self.jogador.rect.x -= self.jogador.direcao.x * self.jogador.velocidade
            self.jogador.rect.y -= self.jogador.direcao.y * self.jogador.velocidade


    def draw(self):
        self.camera_group.center_alvo_camera(self.jogador)
        
        self.window.fill(constantes.PRETO)

        # aplicacao do offset da camera para efeito de paralax
        parallax_speed = 1
        camera_offset_x = self.camera_group.offset.x * parallax_speed
        
        # desenha o primeiro background
        self.window.blit(self.fundo_normal, (self.fundo_x - camera_offset_x, 0))
        
        # desenha o segundo background
        self.window.blit(self.fundo_normal, (self.fundo_x + self.fundo_largura - camera_offset_x, 0))

        # rolagem do background
        velocidade_rolagem = -2
        self.fundo_x += velocidade_rolagem
        if self.fundo_x < -self.fundo_largura:
            self.fundo_x = 0
            
        # mapa principal com offset 
        mapa_pos_ajustada = self.camera_group.get_offset_pos(0, 0)
        self.window.blit(self.mapa_do_jogo, mapa_pos_ajustada)
        
        # desenho de todos os sprites
        self.camera_group.custom_draw(self.jogador) 
        

    def update(self):
        self.jogador.update()
        self.checar_colisao()
        
        # transicoes de tela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'SAIR'
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                    return 'SAIR'
                if keys[pygame.K_a]:
                    return 'GAMEOVER' 
                if keys[pygame.K_v]:
                    return 'VITORIA' 
                    
        return 'JOGO'