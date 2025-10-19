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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return 'SAIR'
            if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                return 'JOGO'  # pode ir direto pro jogo também
        return None

    def update(self,dt):
        # atualiza os sprites - chama Jogador.update() para movimentar
        # self.grupo_sprites.update()
        self.camera_grupo.update(dt) 
                    
        return 'MAPA'