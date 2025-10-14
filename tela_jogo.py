import pygame
from sprites import Jogador

# elementos jogaveis e logica de interacao
class TelaJogo:
    def __init__(self, window, assets):
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
        self.window.fill((0, 0, 0))
        # desenha as sprites na tela
        self.todos_os_sprites.draw(self.window)

    def update(self):
        # atualiza as sprites
        self.todos_os_sprites.update()

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