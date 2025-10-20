from constantes import *

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
        self.velocidade = 5

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
        self.rect.right = min(MAP_W, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(MAP_H, self.rect.bottom)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale_by(surf, SCALE_FACTOR)
        self.rect = self.image.get_rect(topleft = pos)

class Jogador(Sprite):
    def __init__(self, window, assets, pos, groups, collision_sprites, mundo_w, mundo_h, grupo_escadas):
        surf = pygame.Surface((10,10))
        super().__init__(pos, surf, groups)

        self.window = window
        self.assets = assets

        self.mundo_w = mundo_w
        self.mundo_h = mundo_h

        self.vidas = assets['vidas_max']

        # receber dicionario de animacoes
        self.animacoes = assets['animacoes_jogador']
        self.direcao_atual = 'right' # inicial
        self.movendo = False
        self.frame_index = 0
        self.animacao_timer = 0.0
        self.VELOCIDADE_ANIMACAO = 0.1 # troca de quadros

        self.image = self.animacoes[self.direcao_atual][self.frame_index]

        # rect do jogador
        self.rect = self.image.get_rect(center = pos)

        # movimento & colisao
        self.direcao = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.velocidade = 400
        self.gravidade = 50
        self.no_chao = False

        # escada
        self.grupo_escadas = grupo_escadas
        self.subindo_escada = False     
        self.alvo_escada_x = None        
        self.velocidade_subida = 120   

    def reset_state(self):
        self.direcao.x = 0
        self.direcao.y = 0 # Zera a velocidade vertical para evitar queda imediata
        self.subindo_escada = False
        self.alvo_escada_x = None
        self.movendo = False
        self.frame_index = 0
        self.animacao_timer = 0.0
        # O estado 'no_chao' será redefinido pelo próximo ciclo de colisão
        pass
    
    def input(self):
        keys = pygame.key.get_pressed()
        self.movendo = False
        self.direcao.x = 0

        self.subir_tecla = False
        self.descer_tecla = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if not self.subindo_escada:
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    self.direcao.x = -1
                    self.direcao_atual = 'left'
                    self.movendo = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if not self.subindo_escada:
                self.direcao.x = 1
                self.direcao_atual = 'right'
                self.movendo = True
        
        if keys[pygame.K_SPACE] and self.no_chao and not self.subindo_escada:
            self.direcao.y = -20
        
        if keys[pygame.K_UP]:
            self.subir_tecla = True
        if keys[pygame.K_DOWN]:
            self.descer_tecla = True
    
    def verificar_tocando_escada(self):
        if not self.grupo_escadas:
            return None
        zona = self.rect.inflate(-10, -2)  # ajuste esses valores conforme necessário
        for esc in self.grupo_escadas:
            if zona.colliderect(esc.rect):
                return esc
        return None

    def move(self, dt):
        keys = pygame.key.get_pressed()

        # horizontal
        if not self.subindo_escada:
            self.rect.x += self.direcao.x * self.velocidade * dt
            self.collision('horizontal')
        else:
            if self.alvo_escada_x is not None:
                atual_x = float(self.rect.x)
                alvo_x = float(self.alvo_escada_x)
                novo_x = atual_x + (alvo_x - atual_x) * 0.25  

                self.rect.x = int(round(novo_x))

        # vertical
        self.no_chao = False
        tocando_escada = self.verificar_tocando_escada()

        if tocando_escada and (self.subir_tecla or self.descer_tecla):
            if not self.subindo_escada:
                escada_rect = tocando_escada.rect
                self.alvo_escada_x = escada_rect.centerx - self.rect.width // 2
            self.subindo_escada = True

        # sair da escada: se estava subindo mas não está mais tocando
        if self.subindo_escada and not tocando_escada:
            self.subindo_escada = False
            self.alvo_escada_x = None

        # movimento vertical dependendo do estado
        if self.subindo_escada:
            # cancela a gravidade enquanto sobe/desce
            self.direcao.y = 0

            if self.subir_tecla:
                self.rect.y -= int(self.velocidade_subida * dt)
                self.movendo = True

                # verificacao de colisao com o teto ao subir:
                for sprite in self.collision_sprites:
                    if sprite.rect.colliderect(self.rect):
                        self.rect.top = sprite.rect.bottom
                        self.subindo_escada = False
                        self.alvo_escada_x = None
                        
            elif self.descer_tecla:
                self.rect.y += int(self.velocidade_subida * dt)
                self.movendo = True
            else:
                self.movendo = False
            
            if self.descer_tecla: # verifica colisao com o chao só quando desce a escada
                for sprite in self.collision_sprites:
                    if sprite.rect.colliderect(self.rect):
                        
                        if self.rect.bottom > sprite.rect.top: 
                            self.rect.bottom = sprite.rect.top
                            self.direcao.y = 0
                            self.no_chao = True
                            
                            # sai do modo escada
                            self.subindo_escada = False
                            self.alvo_escada_x = None
                            break
            
            if not tocando_escada:
                 self.subindo_escada = False
                 self.alvo_escada_x = None

        else:
            self.direcao.y += self.gravidade * dt
            self.rect.y += int(self.direcao.y)
            self.collision('vertical')
            
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
    
    def collision(self, direcao):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direcao == 'horizontal':
                    if self.direcao.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direcao.x < 0:
                        self.rect.left = sprite.rect.right
                if direcao == 'vertical':
                    if self.subindo_escada:
                        continue
                    if self.direcao.y > 0:
                        # caindo -> posiciona em cima do bloco
                        self.rect.bottom = sprite.rect.top
                        self.direcao.y = 0
                        self.no_chao = True
                    if self.direcao.y < 0:
                        # subindo -> posiciona abaixo do teto
                        self.rect.top = sprite.rect.bottom
                        self.direcao.y = 0

    def limitar_mundo(self):
        # limitacao horizontal 
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.mundo_w:
            self.rect.right = self.mundo_w
            
        # limitacao vertical
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.mundo_h:
            # por enquanto só limita a borda inferior 
            self.rect.bottom = self.mundo_h
            self.direcao.y = 0  # zera velocidade vertical para parar a queda
            self.no_chao = True # assume que ele toca no limite inferior 

    def update(self, dt):
        self.input()
        self.move(dt)
        self.limitar_mundo()

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