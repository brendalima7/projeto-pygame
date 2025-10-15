import pygame
from sprites import Jogador
from cameras import CameraGroup
import constantes

class TelaJogo:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets
        self.jogador = Jogador(self.window, self.assets)  

        self.fundo_normal = self.assets['fundo_mundonormal']
        self.fundo_largura = self.fundo_normal.get_width() # Largura da imagem do fundo
        self.fundo_x = 0 # Posição X inicial do fundo

        self.mapa_do_jogo = self.assets['mapa_do_jogo']

    def draw(self):
        self.window.fill(constantes.PRETO)

        # 1. Define a velocidade de rolagem (pode ajustar esse valor para mais rápido/lento)
        velocidade_rolagem = 0 
        
        # Atualiza a posição X do fundo
        self.fundo_x += velocidade_rolagem

        # Reseta a posição X para criar o efeito de loop contínuo
        # Quando a primeira imagem sair da tela, reposiciona para 0.
        if self.fundo_x < -self.fundo_largura:
            self.fundo_x = 0

        # Desenha a primeira imagem do fundo
        self.window.blit(self.fundo_normal, (self.fundo_x, 0))
        
        # Desenha a segunda imagem do fundo, logo ao lado da primeira,
        # para garantir a continuidade quando a primeira rolar para fora da tela.
        self.window.blit(self.fundo_normal, (self.fundo_x + self.fundo_largura, 0))

        self.window.blit(self.mapa_do_jogo, (0,0))
        self.jogador.draw() 
       

    def update(self):
        # tratamento de eventos - apenas transicoes de tela
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