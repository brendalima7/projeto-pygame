# ARQUIVO: sprites.py

import pygame
import constantes

class Jogador (pygame.sprite.Sprite):
    def __init__(self, window, assets, posicao, grupo):
        super().__init__(grupo)
        self.window = window
        self.assets = assets
        self.image = assets['jogador']
        # retangulo do jogador, posicionado no 'posicao' (centro)
        self.rect = self.image.get_rect(center = posicao)

        self.direcao = pygame.math.Vector2()
        self.velocidade = 5

    def get_input(self):
        keys = pygame.key.get_pressed()

        # REINICIA A DIREÇÃO EM CADA FRAME
        # ESSENCIAL: Garante que o jogador pare de se mover se nenhuma tecla estiver pressionada
        self.direcao.x = 0
        self.direcao.y = 0

        # MOVIMENTO HORIZONTAL
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direcao.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direcao.x = 1

        # MOVIMENTO VERTICAL
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direcao.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direcao.y = 1

    def update(self):
        self.get_input()

        # MOVIMENTO
        # Normaliza a direção: impede que o movimento diagonal seja mais rápido
        if self.direcao.length() != 0:
            self.direcao = self.direcao.normalize()
        
        # Aplica o movimento ao retângulo (posição)
        self.rect.centerx += self.direcao.x * self.velocidade
        self.rect.centery += self.direcao.y * self.velocidade

        # LIMITAÇÃO DE MUNDO: Impede o jogador de sair das bordas do mapa
        # Usa MAP_W e MAP_H das constantes
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(constantes.MAP_W, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(constantes.MAP_H, self.rect.bottom)

    # O método draw é redundante, pois a CameraGroup o substitui (mas mantemos ele vazio)
    def draw(self):
        pass