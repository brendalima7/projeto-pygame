import pygame
from pytmx.util_pygame import load_pygame
from os.path import join
from sprites import *
from cameras import *
from constantes import *

class TelaJogo:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets

        self.collision_sprites = pygame.sprite.Group()
        self.grupo_escadas = pygame.sprite.Group()
        self.grupo_monstros = pygame.sprite.Group() 
        self.grupo_items = pygame.sprite.Group()
        
        self.jogador = None

        self.spawn_point = None 
        self.grupo_agua = pygame.sprite.Group()

        # variaveis para o ciclo de gravidade
        self.gravidade_invertida = False
        self.tempo_inicio_estado = None 
        self.intervalo_mudanca = tempo_mudanca_gravidade # Definido em constantes.py
        
        # varivael para rastrear a chave da imagem de fundo atual
        self.fundo = 'fundo_mundonormal'
        # inventario: lista de dicts {'tipo': str, 'image': Surface}
        self.inventario = []
        self.mostrar_inventario = False
        
        # load game
        self.setup()
        
        # garante que o jogador já está com a gravidade e pulo iniciais
        if self.jogador:
            self.jogador.set_gravidade(gravidade_normal, velocidade_y)

    def iniciar_tempo_gravidade(self):
        self.tempo_inicio_estado = pygame.time.get_ticks()

    def setup(self):
        tmx_mapa = load_pygame(join('data', 'mapa_teste.tmx'))

        map_pixel_width = tmx_mapa.width * TILE_SIZE
        map_pixel_height = tmx_mapa.height * TILE_SIZE
        
        self.all_sprites = CameraGroup(map_pixel_width, map_pixel_height)

        for x, y, imagem in tmx_mapa.get_layer_by_name('Principal').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, (self.all_sprites, self.collision_sprites))
        for x, y, imagem in tmx_mapa.get_layer_by_name('Decoracao2').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, self.all_sprites) 
        
        player_data = None
        monster_data = [] 

        limites_por_tipo = {}

        for objeto in tmx_mapa.get_layer_by_name('Entities'):
            
            obj_name = objeto.name
            
            x_scaled = objeto.x * SCALE_FACTOR
            y_scaled = objeto.y * SCALE_FACTOR
            width_scaled = objeto.width * SCALE_FACTOR
            
            if obj_name == 'Player':
                player_data = ((x_scaled, y_scaled), map_pixel_width, map_pixel_height)
            
            elif obj_name == 'Monstro': 
                
                # limite de patrulha
                min_x_limite = x_scaled
                max_x_limite = x_scaled + width_scaled
                limites_patrulha = (min_x_limite, max_x_limite)
                
                # posico de spawn
                spawn_pos = (x_scaled, y_scaled) 
                
                if obj_name not in limites_por_tipo:
                    min_x_limite = x_scaled
                    max_x_limite = x_scaled + width_scaled
                    limites_patrulha_compartilhados = (min_x_limite, max_x_limite)
                    limites_por_tipo[obj_name] = limites_patrulha_compartilhados
                
                # Recupera os limites para este monstro
                limites_usados = limites_por_tipo[obj_name]

                monster_data.append({
                    'name': obj_name,
                    'pos': spawn_pos,
                    'limites': limites_usados
                })

        # instancia o jogador
        if player_data:
            player_pos, map_w, map_h = player_data
            self.spawn_point = player_pos
            self.jogador = Jogador(
                self.window, self.assets, player_pos,
                self.all_sprites, self.collision_sprites,
                map_w, map_h, 
                self.grupo_escadas
            )

        if self.jogador: # so instancia se o jogador foi criado
            for data in monster_data:
                monstro = Monstro(
                    data['pos'], 
                    (self.all_sprites, self.grupo_monstros), 
                    self.assets, 
                    self.collision_sprites, 
                    data['limites'],
                    self.jogador, 
                    self.grupo_monstros
                )
                # garante que o monstro inicie com a gravidade correta
                monstro.set_gravidade(gravidade_normal) 
        
        # O código para água e escada pode permanecer aqui, fora dos loops anteriores
        for x, y, imagem in tmx_mapa.get_layer_by_name('Agua').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, (self.all_sprites, self.grupo_agua))

        for x, y, imagem in tmx_mapa.get_layer_by_name('Escada').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, self.all_sprites, self.grupo_escadas) 
        # Carrega itens da layer 'Items' (se existir) — espera tiles com gid e propriedades name
        try:
            layer_items = tmx_mapa.get_layer_by_name('Items')
        except Exception:
            layer_items = None

        if layer_items:
            for objeto in layer_items:
                # objetos desta layer no TMX geralmente têm name e gid
                nome = getattr(objeto, 'name', None)
                gid = getattr(objeto, 'gid', None)
                if gid is None:
                    continue
                # obtém a imagem do gid via pytmx
                try:
                    imagem = tmx_mapa.get_tile_image_by_gid(gid)
                except Exception:
                    imagem = None
                if imagem is None:
                    continue

                x_scaled = objeto.x * SCALE_FACTOR
                y_scaled = objeto.y * SCALE_FACTOR

                # instancia Item (classe definida em sprites.py)
                try:
                    Item((x_scaled, y_scaled), imagem, nome, self.all_sprites, self.grupo_items)
                except Exception:
                    # fallback: usar Sprite se Item não estiver disponível
                    Sprite((x_scaled, y_scaled), imagem, (self.all_sprites,))
            
    def jogador_vivo (self):
        self.jogador.vidas -= 1
        
        if self.jogador.vidas <= 0:
            # limpa inventario ao morrer
            try:
                self.inventario.clear()
            except Exception:
                self.inventario = []
            return 'GAMEOVER'
        else:
            # reseta a posição do jogador para o ponto de spawn
            self.jogador.rect.topleft = self.spawn_point
            # reseta o estado (velocidade, subindo escada, etc.)
            self.jogador.reset_state() 
            # rarante que a gravidade é resetada para o estado atual do jogo após o respawn
            self.alternar_gravidade(force_state=self.gravidade_invertida) # Força o estado da gravidade atual
            
            return 'JOGO'
            
    # controla alternancia de  gravidade e fundo
    def alternar_gravidade(self, force_state=None):
        if force_state is None: # Se não forçar estado, alterna normalmente
            self.gravidade_invertida = not self.gravidade_invertida
        else: # Se forçar estado, define diretamente
            self.gravidade_invertida = force_state

        if self.gravidade_invertida:
            nova_gravidade = gravidade_invertida
            novo_pulo = velocidade_y_invertido
            self.fundo = 'fundo_mundoinvertido'
        else:
            nova_gravidade = gravidade_normal
            novo_pulo = velocidade_y
            self.fundo = 'fundo_mundonormal'
        
        if self.jogador:
            self.jogador.set_gravidade(nova_gravidade, novo_pulo)
        
        for monstro in self.grupo_monstros:
            monstro.set_gravidade(nova_gravidade)
            
        # reseta o timer 
        if force_state is None:
            self.tempo_inicio_estado = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return 'SAIR'
        if event.type == pygame.KEYDOWN:
            # alterna inventario com I
            if event.key == pygame.K_i:
                # toggle inventario
                self.mostrar_inventario = not self.mostrar_inventario
                return None
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return 'SAIR'
            if event.key == pygame.K_a:
                return 'GAMEOVER' 
            if event.key == pygame.K_v:
                return 'VITORIA' 
        return None
                
    def update(self, dt):
        self.all_sprites.update(dt)

        # checa timer para alternar gravidade
        if self.tempo_inicio_estado is not None:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_inicio_estado >= self.intervalo_mudanca:
                self.alternar_gravidade() 
                
        # checa colisão com a água
        estado_atual = 'JOGO'
        if self.jogador:
            if pygame.sprite.spritecollideany(self.jogador, self.grupo_agua):
                estado_atual = self.jogador_vivo()

            # checa coleta de itens: colisão por rect é suficiente aqui
            itens_coletados = pygame.sprite.spritecollide(self.jogador, self.grupo_items, dokill=False)
            for item in itens_coletados:
                tipo = getattr(item, 'tipo', None)
                # guarda no inventario (mantendo a imagem original para exibir)
                try:
                    # preserva cópia da imagem em escala atual
                    imagem_item = item.image.copy()
                except Exception:
                    imagem_item = None

                self.inventario.append({'tipo': tipo, 'image': imagem_item})

                # remove o item do mapa
                item.kill()
                
        # checa colisão com monstros (pré-filtro por rect, depois mask)
        for monstro in self.grupo_monstros:
            # pré-filtro: se nem os rects se tocam, ignora
            if not self.jogador.rect.colliderect(monstro.rect):
                continue

            # agora temos um rect-overlap: tenta colisão por mask (pixel-perfect)
            mask_overlap = False
            try:
                mask_overlap = pygame.sprite.collide_mask(self.jogador, monstro) is not None
            except Exception:
                # se as masks não existirem por algum motivo, considera false e cairá no branch de dano por rect
                mask_overlap = False

            # pega prev_rect (fallback para current rect caso não exista)
            prev = getattr(self.jogador, 'prev_rect', self.jogador.rect)

            # parâmetros
            LAND_TOLERANCE = 10
            HORIZ_ALIGN_FACTOR = 0.6

            largura_rel = max(monstro.rect.width, self.jogador.rect.width)
            alinhado_horizontal = abs(self.jogador.rect.centerx - monstro.rect.centerx) <= largura_rel * HORIZ_ALIGN_FACTOR

            if mask_overlap:
                if self.jogador.gravidade_valor > 0:
                    came_from_above = prev.bottom <= monstro.rect.top
                    now_overlaps = self.jogador.rect.bottom >= monstro.rect.top - LAND_TOLERANCE
                    moving_towards = self.jogador.direcao.y > 0
                    is_landing = came_from_above and now_overlaps and moving_towards and alinhado_horizontal
                else:
                    came_from_below = prev.top >= monstro.rect.bottom
                    now_overlaps = self.jogador.rect.top <= monstro.rect.bottom + LAND_TOLERANCE
                    moving_towards = self.jogador.direcao.y < 0
                    is_landing = came_from_below and now_overlaps and moving_towards and alinhado_horizontal

                if is_landing:
                    monstro.kill()
                    # ricochete: força o sinal dependendo da gravidade
                    sinal = -1 if self.jogador.gravidade_valor < 0 else 1
                    # usa o valor absoluto da velocidade_y para garantir direção correta
                    try:
                        self.jogador.direcao.y = sinal * (abs(self.jogador.velocidade_y) / 2)
                    except Exception:
                        self.jogador.direcao.y = 0
                    continue

                # se houve overlap de mask mas não foi landing, é dano
                estado_atual = self.jogador_vivo()
                break

            else:
                # nao houve overlap de mask, mas houve overlap de rect -> tratar como dano 
                estado_atual = self.jogador_vivo()
                break


        return estado_atual

        
    def draw(self):
        self.window.fill(COR_FUNDO)
        
        # usa custom_draw com a câmera seguindo o jogador
        if self.jogador:
            # pega a imagem de fundo correta do assets e passa para o custom_draw
            fundo_atual = self.assets[self.fundo]
            self.all_sprites.custom_draw(self.jogador, fundo_atual)
            
            # desenha vidas 
            vidas_restantes = self.jogador.vidas
            texto_coracoes = chr(9829) * vidas_restantes
            img_cor = self.assets['fonte'].render(texto_coracoes, True, (255, 0, 0)) 
            self.window.blit(img_cor, (10, 10))
            
            # desenha só quando o jogo começa
            if self.tempo_inicio_estado is not None:
                tempo_decorrido_ms = pygame.time.get_ticks() - self.tempo_inicio_estado
                tempo_restante_s = max(0, (self.intervalo_mudanca - tempo_decorrido_ms) / 1000)
                texto_tempo = f"MUDANÇA EM: {tempo_restante_s:.1f}s"
                img_tempo = self.assets['fonte'].render(texto_tempo, True, (255, 255, 255))
                
                # posição do texto tempo
                pos_x = self.window.get_width() // 2 - img_tempo.get_width() // 2
                self.window.blit(img_tempo, (pos_x, 10))
            # desenha inventario se toggled
            if self.mostrar_inventario:
                # janela simples semi-transparente
                inv_w, inv_h = 400, 200
                inv_surf = pygame.Surface((inv_w, inv_h), pygame.SRCALPHA)
                inv_surf.fill((0, 0, 0, 180))
                inv_x = self.window.get_width()//2 - inv_w//2
                inv_y = self.window.get_height()//2 - inv_h//2
                # desenha título
                titulo = self.assets['fonte2'].render('INVENTARIO', True, (255,255,255))
                inv_surf.blit(titulo, (10, 10))

                # desenha thumbnails
                padding = 10
                thumb_size = 48
                x = padding
                y = 40
                for entry in self.inventario:
                    img = entry.get('image')
                    if img:
                        # redimensiona para thumb_size mantendo proporção
                        try:
                            thumb = pygame.transform.scale(img, (thumb_size, thumb_size))
                        except Exception:
                            thumb = pygame.Surface((thumb_size, thumb_size))
                            thumb.fill((100,100,100))
                    else:
                        thumb = pygame.Surface((thumb_size, thumb_size))
                        thumb.fill((100,100,100))

                    inv_surf.blit(thumb, (x, y))
                    x += thumb_size + padding
                    if x + thumb_size + padding > inv_w:
                        x = padding
                        y += thumb_size + padding

                # blit janela completa na janela principal
                self.window.blit(inv_surf, (inv_x, inv_y))
            
        else:
            self.all_sprites.draw(self.window)
    
    def restart(self):
        # limpa grupos antigos (se existirem)
        try:
            if hasattr(self, 'all_sprites'):
                self.all_sprites.empty()
        except Exception:
            pass

        # grupos que criamos em setup()
        self.collision_sprites.empty()
        self.grupo_escadas.empty()
        self.grupo_monstros.empty()
        self.grupo_agua.empty()
        self.grupo_items.empty()
        # limpa inventario também no restart
        try:
            self.inventario.clear()
        except Exception:
            self.inventario = []

        # opcional: zera variáveis de controle de tempo/gravidade
        self.tempo_inicio_estado = None
        self.gravidade_invertida = False
        self.fundo = 'fundo_mundonormal'

        # chama setup() para recriar mapa, sprites, jogador e monstros
        self.setup()

        # garante que o jogador criado em setup() comece com valores padrão
        if self.jogador:
            self.jogador.vidas = self.assets.get('vidas_max', self.jogador.vidas)
            self.jogador.set_gravidade(gravidade_normal, velocidade_y)
            # posiciona no spawn (setup já define spawn_point e jogador)
            self.jogador.rect.topleft = self.spawn_point

        # reinicia timer de gravidade (se desejar começar o ciclo imediatamente)
        self.iniciar_tempo_gravidade()  