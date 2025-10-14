import pygame
import constantes

class Jogador (pygame.sprite.Sprite):
    def __init__(self, window, assets, velocidade):

        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.assets = assets
        self.image = assets['jogador']
        # retangulo do jogador
        self.rect = self.image.get_rect()

        # posicao inicial do retangulo ( no centro da tela )
        self.rect.center = (constantes.WINDOWWIDHT/2, constantes.WINDOWHEIGHT/2)

        # velocidade do jogador 
        self.velocidade = velocidade
        self.x = 0
        self.y = 0

    def get_input(self):
        keys = pygame.key.get_pressed()

        # garante que ao soltar a tecla o jogador para
        self.x = 0
        self.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = -self.velocidade
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = self.velocidade
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y = -self.velocidade
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y = self.velocidade

    def update(self):
        self.get_input()
        # movimento 
        self.rect.x += self.x
        self.rect.y += self.y

    def draw(self):
        # desenha a imagem do jogador dentro do retangulo
        self.window.blit(self.image, self.rect) 