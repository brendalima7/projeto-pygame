import pygame
from sprites import Jogador # Importando a classe Jogador corrigida
from cameras import CameraGroup
import constantes

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