import pygame
from sprites import Jogador

class TelaMapa:
    def __init__(self,window,assets):
        self.window = window
        self.assets = assets

        velocidade_jogador = 1
        # inicializa o jogador
        self.jogador = Jogador(self.window, self.assets, velocidade_jogador) 
        # grupo de sprites dessa tela
        self.todos_os_sprites = pygame.sprite.Group()
        # adicionar o jogador no grupo 
        self.todos_os_sprites.add(self.jogador) 


    def draw(self):
        self.window.fill((255, 255, 255))
        # desenha as sprites na tela
        self.todos_os_sprites.draw(self.window)

    def update(self):
        # atualiza as sprites
        self.todos_os_sprites.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'SAIR'
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                    return 'SAIR'
                if keys[pygame.K_j]:
                    return 'JOGO'  
        return 'MAPA'