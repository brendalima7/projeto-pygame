import pygame
from sprites import JogadorMapa
from cameras import CameraGroup
import constantes

class TelaMapa: 
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets 
        
        # cria o grupo de camera passando as dimensoes do mapa
        self.camera_grupo = CameraGroup(constantes.MAP_W, constantes.MAP_H)
        
        # cria a superficie do mapa 
        self.map_surface = assets['map_surface']

        # posicao inicial do jogador
        posicao_inicial = (constantes.MAP_W / 2, constantes.MAP_H / 2)
        # passa self.camera_grupo como o grupo para o jogador
        self.jogador = JogadorMapa(self.window, self.assets, posicao_inicial, self.camera_grupo) 
        
    def draw(self):
        self.window.fill(constantes.PRETO)
        
        # desenha tudo (fundo + sprites) usando o custom_draw da camera
        self.camera_grupo.custom_draw(self.jogador, self.map_surface)

    def update(self,dt):
        # atualiza os sprites - chama Jogador.update() para movimentar
        # self.grupo_sprites.update()
        self.camera_grupo.update(dt) 

        # tratamento de eventos para transicao de telas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'SAIR'
            
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                    return 'SAIR'
                
                # exemplo de transicao para o JOGO
                if keys[pygame.K_j]:
                    return 'JOGO' 
                    
        return 'MAPA'