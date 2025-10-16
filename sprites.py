import pygame
import constantes

class JogadorMapa (pygame.sprite.Sprite):
    def __init__(self, window, assets, posicao, grupo):
        super().__init__(grupo)
        self.window = window
        self.assets = assets

        # recebe o dicionario de animacoes
        self.animacoes = assets['animacoes_jogador'] 
        
        self.direcao_atual = 'down' # direcao inicial do jogador 
        self.movendo = False
        self.frame_index = 0
        self.animacao_timer = 0.0 
        self.VELOCIDADE_ANIMACAO = 0.1 # velocidade da trpca de quadros
        
        self.image = self.animacoes[self.direcao_atual][self.frame_index]
        
        # rect do jogador posicionado no 'posicao' (centro)
        self.rect = self.image.get_rect(center = posicao)

        self.direcao = pygame.math.Vector2()
        self.velocidade = 10

    def get_input(self):
        keys = pygame.key.get_pressed()
        self.movendo = False

        # reinicia a direcaoo em cada frame para o jogador parar de se mover se nenhuma tecla estiver pressionada
        self.direcao.x = 0
        self.direcao.y = 0

        # movimento x
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direcao.x = -1
            self.direcao_atual = 'left'
            self.movendo = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direcao.x = 1
            self.direcao_atual = 'right'
            self.movendo = True

        # movimento y
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direcao.y = -1
            self.direcao_atual = 'up'
            self.movendo = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direcao.y = 1
            self.direcao_atual = 'down'
            self.movendo = True

    def update(self, dt):
        self.get_input()

        # normaliza direcao - impede que o movimento diagonal seja mais rápido
        if self.direcao.length() != 0:
            self.direcao = self.direcao.normalize()
        
        # aplica o movimento ao rect
        self.rect.centerx += self.direcao.x * self.velocidade
        self.rect.centery += self.direcao.y * self.velocidade
        
        if self.movendo:
            # troca de Frame: se movendo, incrementa o timer
            self.animacao_timer += dt
            
            # se o tempo para o proximo frame é atingido:
            if self.animacao_timer >= self.VELOCIDADE_ANIMACAO:
                self.animacao_timer = 0.0
                
                # avanca para o próximo frame - loop
                num_frames = len(self.animacoes[self.direcao_atual])
                self.frame_index = (self.frame_index + 1) % num_frames
        else:
            # definindo a imagem 0 para pose parada em cada direcao de animacao 
            self.frame_index = 0
            self.animacao_timer = 0.0 # reseta o timer
            
        # atualiza a imagem desenhada na tela
        self.image = self.animacoes[self.direcao_atual][self.frame_index]
        
        # impede o jogador de sair das bordas do mapa
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(constantes.MAP_W, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(constantes.MAP_H, self.rect.bottom)

class Jogador(pygame.sprite.Sprite):
    def __init__(self, window, assets):
        super().__init__()
        
        self.window = window
        self.assets = assets
        
        self.image = assets['jogador_mapa'] 
        
        # define o atributo self.rect a partir da imagem
        self.rect = self.image.get_rect()
        
        # posicao inicial do jogador no mundo
        self.rect.x = 1500 
        self.rect.y = 2000
        
        self.direcao = pygame.math.Vector2()
        self.velocidade = 5 
        
    def get_input(self):
        keys = pygame.key.get_pressed()

        self.direcao.x = 0
        self.direcao.y = 0
        
        # movimento em x
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direcao.x = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direcao.x = 1

        # movimento em y
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direcao.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direcao.y = 1

    def update(self):
        # atualiza posicao do jogador e aplica limites
        self.get_input()

        # movimento
        if self.direcao.length() != 0:
            self.direcao = self.direcao.normalize()
        
        self.rect.x += self.direcao.x * self.velocidade
        self.rect.y += self.direcao.y * self.velocidade

        # limites do mapa
        MAP_W_FASE = 5000 
        MAP_H_FASE = 2500

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(MAP_W_FASE, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(MAP_H_FASE, self.rect.bottom)