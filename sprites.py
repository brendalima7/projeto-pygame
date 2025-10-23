from constantes import *


"""
Módulo de sprites do jogo SWITCH BACK.

Contém as classes:
- Sprite: base para sprites com escala automática.
- Item: item coletável que herda de Sprite.
- Jogador: lógica do jogador (movimento, física, escadas, colisões).
- Monstro: entidade inimiga com IA simples e comportamento de patrulha/perseguição.
"""

class Sprite(pygame.sprite.Sprite):
    """Classe base para todas as sprites do jogo.

    Gerencia a escala da imagem com `SCALE_FACTOR` e a criação do rect.
    Aceita um número variável de grupos (`*groups`) que serão adicionados via
    `super().__init__(*groups)` (comportamento padrão do pygame).
    """

    def __init__(self, pos, surf, *groups):
        """Inicializa a sprite base.

        Args:
            pos (tuple): Posição (x, y) do canto superior esquerdo onde a sprite será colocada.
            surf (pygame.Surface): Surface original que será escalada.
            *groups: Grupos do pygame.sprite.Group aos quais esta sprite será adicionada.
        """
        super().__init__(*groups)
        self.image = pygame.transform.scale_by(surf, SCALE_FACTOR)
        self.rect = self.image.get_rect(topleft = pos)

    def draw(self, surface, offset=(0,0)):
        """Desenha a sprite na surface aplicando o offset da câmera.

        Args:
            surface (pygame.Surface): Superfície onde desenhar a sprite.
            offset (tuple|pygame.math.Vector2): Deslocamento da câmera (x, y).
        """
        # Garante que offset seja Vector2 para subtração
        off = pygame.math.Vector2(int(offset[0]), int(offset[1])) if not isinstance(offset, pygame.math.Vector2) else offset
        pos = pygame.math.Vector2(self.rect.topleft) - off
        surface.blit(self.image, (int(pos.x), int(pos.y)))


class Item(Sprite):
    """Um item coletável no mapa.

    Guarda o tipo (ex.: 'shield') e reutiliza a lógica de escala/rect da classe Sprite.
    """
    def __init__(self, pos, surf, tipo, *groups):
        """Inicializa um item.

        Args:
            pos (tuple): Posição do item.
            surf (pygame.Surface): Imagem do tile/item.
            tipo (str): Identificador do tipo de item (ex.: 'shield').
            *groups: Grupos aos quais o item será adicionado.
        """
        # surf deve ser uma Surface (normalmente obtida via pytmx)
        super().__init__(pos, surf, *groups)
        self.tipo = tipo

class Jogador(Sprite):
    """Representa o jogador com física, animação e interação com o mundo.

    Implementa:
    - movimento horizontal e vertical (com gravidade customizável);
    - controle de pulos considerando gravidade invertida;
    - interação com escadas (subir/descer);
    - colisões horizontais e verticais;
    - animação por frames dependendo do estado;
    - armazenamento de estado para respawn.
    """
    def __init__(self, window, assets, pos, groups, collision_sprites, mundo_w, mundo_h, grupo_escadas):
        """Inicializa o jogador.

        Args:
            window (pygame.Surface): Superfície principal do jogo.
            assets (dict): Dicionário de assets (animações, sons, fontes).
            pos (tuple): Posição inicial do jogador (centro).
            groups: Grupos onde a entidade será adicionada (passado adiante a Sprite).
            collision_sprites (Group): Grupos usados para checagem de colisão.
            mundo_w (int): Largura do mundo em pixels.
            mundo_h (int): Altura do mundo em pixels.
            grupo_escadas (Group): Grupo contendo sprites de escada.
        """
        surf = pygame.Surface((10,10)) # O surf inicial não importa muito, pois a imagem é substituída
        super().__init__(pos, surf, groups)

        self.window = window
        self.assets = assets

        self.mundo_w = mundo_w
        self.mundo_h = mundo_h

        self.vidas = assets['vidas_max']

        # receber dicionario de animacoes
        self.animacoes = assets['animacoes_jogador']
        
        self.animacoes_invertidas = {}
        for key, frames in self.animacoes.items():
            # cria lista de frames virados de cabeça para baixo (flip vertical)
            self.animacoes_invertidas[key] = [pygame.transform.flip(f, False, True) for f in frames]

        self.direcao_atual = 'right' # inicial
        self.movendo = False
        self.frame_index = 0
        self.animacao_timer = 0.0
        self.VELOCIDADE_ANIMACAO = 0.1 # troca de quadros

        # usa o frame inicial normal (gravidade inicial é definida abaixo)
        self.image = self.animacoes[self.direcao_atual][self.frame_index]

        # rect do jogador
        self.rect = self.image.get_rect(center = pos)

        # movimento & colisao
        self.direcao = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.velocidade = 400
        
        # NOVO: Gravidade e velocidade de pulo são atributos do jogador
        self.gravidade_valor = gravidade_normal # Começa com gravidade normal
        self.velocidade_y = velocidade_y # Começa com pulo normal
        
        self.no_chao = False # Indica se o jogador está em uma superfície

        # escada
        self.grupo_escadas = grupo_escadas
        self.subindo_escada = False
        self.alvo_escada_x = None
        self.velocidade_subida = 120

    def set_gravidade(self, nova_gravidade, nova_velocidade_y):
        """Define gravidade e velocidade de pulo do jogador.

        Args:
            nova_gravidade (float): Valor da gravidade a aplicar.
            nova_velocidade_y (float): Velocidade de salto correspondente.
        """
        self.gravidade_valor = nova_gravidade
        self.velocidade_y = nova_velocidade_y
        self.direcao.y = 0
        self.no_chao = False

    def reset_state(self):
        """Reset parcial do estado do jogador sem reposicionar.

        Uso típico: após perder vida e dar respawn mantendo spawn_point.
        """
        self.direcao.x = 0
        self.direcao.y = 0 
        self.subindo_escada = False
        self.alvo_escada_x = None
        self.movendo = False
        self.frame_index = 0
        self.animacao_timer = 0.0
        self.no_chao = False # Garante que ao resetar, não está no chão
        # A gravidade será redefinida pela TelaJogo no método alternar_gravidade
    
    def input(self):
        """Lê o estado do teclado e atualiza intenções de movimento/pulo/escada."""
        keys = pygame.key.get_pressed()
        self.movendo = False
        self.direcao.x = 0

        self.subir_tecla = False
        self.descer_tecla = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direcao.x = -1
            self.direcao_atual = 'left'
            self.movendo = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direcao.x = 1
            self.direcao_atual = 'right'
            self.movendo = True

        if keys[pygame.K_SPACE] and self.no_chao and not self.subindo_escada:
            self.direcao.y = self.velocidade_y
            # toca som de pulo
            footstep = self.assets.get('footstep_sound')
            if footstep:
                footstep.play()

        # marcar intenção de subir/descer escada
        if keys[pygame.K_UP]:
            self.subir_tecla = True
        if keys[pygame.K_DOWN]:
            self.descer_tecla = True

        # Permitir sair da escada a qualquer momento
        # Se estiver subindo escada e o jogador pressionar esquerda/direita, sair da escada
        if self.subindo_escada and (keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.subindo_escada = False
            self.alvo_escada_x = None
            # direcao.x já foi ajustada acima conforme a tecla pressionada
            self.movendo = True

        # Se estiver subindo escada e pressionar pular (SPACE), sai da escada e aplica pulo
        if self.subindo_escada and keys[pygame.K_SPACE]:
            self.subindo_escada = False
            self.alvo_escada_x = None
            self.direcao.y = self.velocidade_y
    
    def verificar_tocando_escada(self):
        """Retorna a escada (sprite) com a qual o jogador está em contato, se houver."""
        if not self.grupo_escadas:
            return None
        zona = self.rect.inflate(-10, -2)
        for esc in self.grupo_escadas:
            if zona.colliderect(esc.rect):
                return esc
        return None

    def move(self, dt):
        """Executa movimento horizontal e vertical, tratando escadas e colisões.

        Args:
            dt (float): Delta time em segundos.
        """
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
        self.no_chao = False # Reseta o estado no_chao em cada frame
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
            self.direcao.y = 0 # cancela a gravidade enquanto sobe/desce
            if self.subir_tecla:
                self.rect.y -= int(self.velocidade_subida * dt)
                self.movendo = True
                # verificação de colisão com o teto ao subir:
                for sprite in self.collision_sprites:
                    if sprite.rect.colliderect(self.rect):
                        # Se a gravidade é normal, o "teto" é top. Se invertida, o "chão" é top.
                        if self.gravidade_valor > 0: # Gravidade normal
                            self.rect.top = sprite.rect.bottom
                        else: # Gravidade negativa
                            self.rect.bottom = sprite.rect.top 
                        self.subindo_escada = False
                        self.alvo_escada_x = None
                        
            elif self.descer_tecla:
                self.rect.y += int(self.velocidade_subida * dt)
                self.movendo = True
            else:
                self.movendo = False
            
            # verificação de colisão com o chão (apenas ao descer a escada)
            if self.descer_tecla: 
                for sprite in self.collision_sprites:
                    if sprite.rect.colliderect(self.rect):
                        # Se a gravidade é normal, o "chão" é bottom. Se invertida, o "teto" é bottom.
                        if self.gravidade_valor > 0: # Gravidade normal
                            self.rect.bottom = sprite.rect.top
                        else: # Gravidade negativa
                            self.rect.top = sprite.rect.bottom

                        self.direcao.y = 0
                        self.no_chao = True
                        self.subindo_escada = False
                        self.alvo_escada_x = None
                        break
        else:
            self.direcao.y += self.gravidade_valor * dt
            self.rect.y += int(self.direcao.y)
            self.collision('vertical')
            
        self.rect.x = int(self.rect.x)
        self.rect.y = int(self.rect.y)
    
    def collision(self, direcao):
        """Trata colisões com sprites de colisão para as direções horizontal/vertical.

        Args:
            direcao (str): 'horizontal' ou 'vertical'.
        """
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direcao == 'horizontal':
                    if self.direcao.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direcao.x < 0:
                        self.rect.left = sprite.rect.right
                if direcao == 'vertical':
                    if self.subindo_escada: # Já tratada na lógica da escada
                        continue
                        
                    # Verifica se está caindo (na direção da gravidade)
                    is_falling = (self.gravidade_valor > 0 and self.direcao.y > 0) or \
                                 (self.gravidade_valor < 0 and self.direcao.y < 0)

                    if is_falling:
                        if self.gravidade_valor > 0: 
                            self.rect.bottom = sprite.rect.top
                        else: 
                            self.rect.top = sprite.rect.bottom
                            
                        self.direcao.y = 0
                        self.no_chao = True
                        
                    # verifica se está pulando/subindo (contra a gravidade)
                    is_jumping = (self.gravidade_valor > 0 and self.direcao.y < 0) or \
                                 (self.gravidade_valor < 0 and self.direcao.y > 0)

                    if is_jumping:
                        # batendo no teto/obstáculo:
                        if self.gravidade_valor > 0: # gravidade normal: bateu no teto
                            self.rect.top = sprite.rect.bottom
                        else: # gravidade negativa: bateu no  "teto" (chao)
                            self.rect.bottom = sprite.rect.top 

                        self.direcao.y = 0

    def limitar_mundo(self):
        """Impõe limites do mapa ao rect do jogador dependendo da gravidade."""
        # limitacao horizontal 
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.mundo_w:
            self.rect.right = self.mundo_w
            
        # limitacao vertical dependendo da gravidade
        if self.gravidade_valor > 0: # gravidade nomeal
            if self.rect.top < 0:
                self.rect.top = 0 
                self.direcao.y = 0 
            elif self.rect.bottom > self.mundo_h:
                self.rect.bottom = self.mundo_h
                self.direcao.y = 0 
                self.no_chao = True 
        else: # gravidade negativa
            if self.rect.bottom > self.mundo_h: # limite inferior
                self.rect.bottom = self.mundo_h
                self.direcao.y = 0 
            elif self.rect.top < 0: 
                self.rect.top = 0
                self.direcao.y = 0
                self.no_chao = True

    def update(self, dt):
        """Atualiza o estado do jogador: entrada, movimento, colisões e animação.

        Args:
            dt (float): Delta time em segundos.
        """
        self.prev_rect = self.rect.copy()

        # comportamento normal do jogador
        self.input()
        self.move(dt)
        self.limitar_mundo()

        # animacao
        if self.movendo:
            self.animacao_timer += dt
            if self.animacao_timer >= self.VELOCIDADE_ANIMACAO:
                self.animacao_timer = 0.0
                # escolhe a lista de frames (normal ou invertida) dependendo do sinal da gravidade
                if self.gravidade_valor < 0:
                    num_frames = len(self.animacoes_invertidas[self.direcao_atual])
                else:
                    num_frames = len(self.animacoes[self.direcao_atual])
                self.frame_index = (self.frame_index + 1) % num_frames
        else:
            self.frame_index = 0
            self.animacao_timer = 0.0
        if self.gravidade_valor < 0:
            frames_list = self.animacoes_invertidas[self.direcao_atual]
        else:
            frames_list = self.animacoes[self.direcao_atual]

        # garante que frame_index está dentro do limite da lista escolhida
        if self.frame_index >= len(frames_list):
            self.frame_index = 0

        # preserva o centro do rect ao trocar a imagem (evita "pulos")
        old_center = self.rect.center
        self.image = frames_list[self.frame_index]
        self.rect = self.image.get_rect(center=old_center)

class Monstro(Sprite):
    """Entidade inimiga com comportamento de patrulha e perseguição.

    Considera água (não atravessa), aplica gravidade e tem pequenas rotinas
    de IA (patrulha/perseguição).
    """
    def __init__(self, pos, groups, assets, collision_sprites, limites_patrulha, jogador_ref, grupo_monstros, water_sprites=None):
        """Inicializa o monstro.

        Args:
            pos (tuple): Posição inicial do monstro.
            groups: Grupos aos quais o monstro pertence.
            assets (dict): Dicionário de assets (animações, sons).
            collision_sprites (Group): Sprites sólidos para colisões.
            limites_patrulha (tuple): (min_x, max_x) para patrulha.
            jogador_ref (Jogador): Referência ao objeto jogador para perseguição.
            grupo_monstros (Group): Grupo de monstros.
            water_sprites (Group | list | None): Sprites/rects representando água.
        """
        surf = pygame.Surface((32, 32)) 
        super().__init__(pos, surf, groups)
        
        self.assets = assets
        self.collision_sprites = collision_sprites
        self.jogador_ref = jogador_ref
        self.grupo_monstros = grupo_monstros

        # water_sprites pode ser None, um pygame.sprite.Group, ou uma lista de sprites/rects
        self.water_sprites = water_sprites

        # animações (pré-invertidas como você já fez antes, se quiser)
        self.animacoes = assets['animacoes_monstro']
        self.animacoes_invertidas = {}
        for key, frames in self.animacoes.items():
            self.animacoes_invertidas[key] = [pygame.transform.flip(f, False, True) for f in frames]

        self.direcao_atual = 'right' 
        self.movendo = True
        self.frame_index = 0
        self.animacao_timer = 0.0
        self.VELOCIDADE_ANIMACAO = 0.15
        self.image = self.animacoes[self.direcao_atual][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        self.direcao = pygame.math.Vector2(1, 0)
        self.velocidade_patrulha = 50
        self.velocidade_perseguicao = 50
        self.velocidade = self.velocidade_patrulha 
        self.gravidade_valor = gravidade_normal
        self.no_chao = False

        self.limites_patrulha = limites_patrulha
        self.raio_de_visao = 400
        self.modo_ia = 'patrulha'

    def set_gravidade(self, nova_gravidade):
        """Define a gravidade do monstro."""
        self.gravidade_valor = nova_gravidade
        self.direcao.y = 0

    def aplicar_gravidade(self, dt):
        """Aplica a física vertical (gravidade) ao monstro com rollback se entrar na água."""
        # Antes de aplicar, guarda a posição anterior para possível rollback
        old_rect = self.rect.copy()
        self.direcao.y += self.gravidade_valor * dt
        self.rect.y += int(self.direcao.y)
        self.collision('vertical')

        # Se acabou dentro de água, volta e zera velocidade vertical (não permite cair na água)
        if self._collide_with_water():
            self.rect = old_rect
            self.direcao.y = 0
            self.no_chao = True

    def _collide_with_water(self):
        """Retorna True se o rect do monstro colidir com qualquer water_rect.

        Aceita self.water_sprites sendo None, Group, list de sprites, ou list de rects.
        """
        if not self.water_sprites:
            return False
        # group de sprites
        if isinstance(self.water_sprites, pygame.sprite.Group):
            return pygame.sprite.spritecollideany(self, self.water_sprites) is not None
        # lista/iterável de sprites ou rects
        for w in self.water_sprites:
            if hasattr(w, 'rect'):
                if self.rect.colliderect(w.rect):
                    return True
            elif isinstance(w, pygame.Rect):
                if self.rect.colliderect(w):
                    return True
        return False

    def _probe_agua_a_frente(self, px_a_frente=4, probe_height=4):
        """Retorna True se ao andar px_a_frente na direção X atual o pé do monstro cairia em água.

        Usa uma pequena caixa (probe) na borda inferior na direção do movimento.
        """
        if not self.water_sprites:
            return False
        # determina onde fica 'pé' dependendo da gravidade
        if self.gravidade_valor > 0:
            # gravidade normal: pé é bottom
            probe_rect = pygame.Rect(0,0, self.rect.width, probe_height)
            if self.direcao.x > 0:
                probe_rect.topleft = (self.rect.right + px_a_frente, self.rect.bottom)
            elif self.direcao.x < 0:
                probe_rect.topright = (self.rect.left - px_a_frente, self.rect.bottom)
            else:
                return False
        else:
            # gravidade invertida: 'pé' é top
            probe_rect = pygame.Rect(0,0, self.rect.width, probe_height)
            if self.direcao.x > 0:
                probe_rect.bottomleft = (self.rect.right + px_a_frente, self.rect.top)
            elif self.direcao.x < 0:
                probe_rect.bottomright = (self.rect.left - px_a_frente, self.rect.top)
            else:
                return False

        # checa colisão do probe com water_sprites
        if isinstance(self.water_sprites, pygame.sprite.Group):
            for w in self.water_sprites:
                if probe_rect.colliderect(w.rect):
                    return True
        else:
            for w in self.water_sprites:
                wrect = w.rect if hasattr(w, 'rect') else w
                if probe_rect.colliderect(wrect):
                    return True
        return False

    def collision(self, direcao):
        """Trata colisões do monstro com o ambiente nas direções horizontal/vertical."""
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direcao == 'horizontal':
                    if self.direcao.x > 0:
                        self.rect.right = sprite.rect.left
                        self.direcao.x *= -1
                    if self.direcao.x < 0:
                        self.rect.left = sprite.rect.right
                        self.direcao.x *= -1
                        
                if direcao == 'vertical':
                    is_falling = (self.gravidade_valor > 0 and self.direcao.y > 0) or \
                                 (self.gravidade_valor < 0 and self.direcao.y < 0)

                    if is_falling:
                        if self.gravidade_valor > 0:
                            self.rect.bottom = sprite.rect.top
                        else:
                            self.rect.top = sprite.rect.bottom
                        self.direcao.y = 0
                        self.no_chao = True
                    else:
                        is_jumping = (self.gravidade_valor > 0 and self.direcao.y < 0) or \
                                     (self.gravidade_valor < 0 and self.direcao.y > 0)
                        if is_jumping:
                            if self.gravidade_valor > 0:
                                self.rect.top = sprite.rect.bottom
                            else:
                                self.rect.bottom = sprite.rect.top
                            self.direcao.y = 0

    def ia_patrulha(self, dt):
        """Lógica simples de patrulha entre limites_patrulha."""
        if self.direcao.x > 0 and self.rect.right >= self.limites_patrulha[1]:
            self.direcao.x = -1
        elif self.direcao.x < 0 and self.rect.left <= self.limites_patrulha[0]:
            self.direcao.x = 1
        self.direcao_atual = 'right' if self.direcao.x > 0 else 'left'

    def ia_perseguicao(self, dt):
        """Ajusta direção para perseguir a posição X do jogador."""
        jogador_x = self.jogador_ref.rect.centerx
        if self.rect.centerx < jogador_x:
            self.direcao.x = 1
            self.direcao_atual = 'right'
        elif self.rect.centerx > jogador_x:
            self.direcao.x = -1
            self.direcao_atual = 'left'
        else:
            self.direcao.x = 0

    def verifica_modo_ia(self):
        """Escolhe modo de IA (patrulha ou perseguição) baseado na distância ao jogador."""
        distancia = abs(self.rect.centerx - self.jogador_ref.rect.centerx)
        if distancia <= self.raio_de_visao:
            self.modo_ia = 'perseguicao'
            self.velocidade = self.velocidade_perseguicao
        else:
            self.modo_ia = 'patrulha'
            self.velocidade = self.velocidade_patrulha

    def update(self, dt):
        """Atualiza o comportamento e animação do monstro.

        Args:
            dt (float): Delta time em segundos.
        """
        self.verifica_modo_ia()

        if self.modo_ia == 'patrulha':
            self.ia_patrulha(dt)
        else:
            self.ia_perseguicao(dt)
            
        # --- Pre-probe: evita andar se tem água à frente ---
        if self._probe_agua_a_frente(px_a_frente=4, probe_height=6):
            # em vez de andar para a água, inverter direção
            self.direcao.x *= -1
        else:
            # movimento horizontal normal: guarda old_rect para rollback caso entre em água
            old_rect = self.rect.copy()
            self.rect.x += self.direcao.x * self.velocidade * dt
            self.collision('horizontal')

            # se após mover o monstro estiver colidindo com água, reverte e inverte direção
            if self._collide_with_water():
                self.rect = old_rect
                self.direcao.x *= -1

        # aplica gravidade/movimento vertical
        self.aplicar_gravidade(dt)
        
        # animacao (mantendo inversão como antes)
        self.animacao_timer += dt
        if self.animacao_timer >= self.VELOCIDADE_ANIMACAO:
            self.animacao_timer = 0.0
            if self.gravidade_valor < 0:
                num_frames = len(self.animacoes_invertidas[self.direcao_atual])
            else:
                num_frames = len(self.animacoes[self.direcao_atual])
            self.frame_index = (self.frame_index + 1) % num_frames

        if self.gravidade_valor < 0:
            frames_list = self.animacoes_invertidas[self.direcao_atual]
        else:
            frames_list = self.animacoes[self.direcao_atual]

        if self.frame_index >= len(frames_list):
            self.frame_index = 0

        old_center = self.rect.center
        self.image = frames_list[self.frame_index]
        self.rect = self.image.get_rect(center=old_center)
