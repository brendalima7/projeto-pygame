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
        self.intervalo_mudanca = tempo_mudanca_gravidade
        
        # [NOVO] Variáveis para o cronômetro de speedrun
        self.tempo_inicio_jogo = 0 
        self.tempo_conclusao = 0 
        
        # varivael para rastrear a chave da imagem de fundo atual
        self.fundo = 'fundo_mundonormal'
        # inventario: lista de dicts {'tipo': str, 'image': Surface}
        self.inventario = []
        self.mostrar_inventario = False
        # contador de shields: total no mapa e coletados
        self.total_shields = 0
        self.shields_coletados = 0
        
        # load game
        self.setup()
        
        if self.jogador:
            self.jogador.set_gravidade(gravidade_normal, velocidade_y) 

    def iniciar_tempo_gravidade(self):
        self.tempo_inicio_estado = pygame.time.get_ticks()
        
        # [CRONÔMETRO] Inicia o cronômetro de speedrun
        self.tempo_inicio_jogo = pygame.time.get_ticks() 
        self.tempo_conclusao = 0

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
        self.final_pos = None

        limites_por_tipo = {}

        for objeto in tmx_mapa.get_layer_by_name('Entities'):
            
            obj_name = objeto.name
            
            x_scaled = objeto.x * SCALE_FACTOR
            y_scaled = objeto.y * SCALE_FACTOR
            width_scaled = objeto.width * SCALE_FACTOR
            
            if obj_name == 'Player':
                player_data = ((x_scaled, y_scaled), map_pixel_width, map_pixel_height)
            
            elif obj_name == 'final':
                tile_img = tmx_mapa.get_tile_image_by_gid(objeto.gid)
                if tile_img:
                    self.final_pos = Sprite((x_scaled, y_scaled), tile_img, self.all_sprites)
            
            elif obj_name == 'Monstro': 
                
                min_x_limite = x_scaled
                max_x_limite = x_scaled + width_scaled
                limites_patrulha = (min_x_limite, max_x_limite)
                
                spawn_pos = (x_scaled, y_scaled) 
                
                if obj_name not in limites_por_tipo:
                    min_x_limite = x_scaled
                    max_x_limite = x_scaled + width_scaled
                    limites_patrulha_compartilhados = (min_x_limite, max_x_limite)
                    limites_por_tipo[obj_name] = limites_patrulha_compartilhados
                
                limites_usados = limites_por_tipo[obj_name]

                monster_data.append({
                    'name': obj_name,
                    'pos': spawn_pos,
                    'limites': limites_usados
                })

        if player_data:
            player_pos, map_w, map_h = player_data
            self.spawn_point = player_pos
            self.jogador = Jogador(
                self.window, self.assets, player_pos,
                self.all_sprites, self.collision_sprites,
                map_w, map_h, 
                self.grupo_escadas
            )

        if self.jogador:
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
                monstro.set_gravidade(gravidade_normal) 
        
        for x, y, imagem in tmx_mapa.get_layer_by_name('Agua').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, (self.all_sprites, self.grupo_agua))

        for x, y, imagem in tmx_mapa.get_layer_by_name('Escada').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, self.all_sprites, self.grupo_escadas) 
            
        layer_items = None
        layer_names = [getattr(layer, 'name', None) for layer in tmx_mapa.layers]
        if 'Items' in layer_names:
            layer_items = tmx_mapa.get_layer_by_name('Items')

        if layer_items:
            for objeto in layer_items:
                nome = getattr(objeto, 'name', None)
                gid = getattr(objeto, 'gid', None)
                if gid is None:
                    continue
                imagem = tmx_mapa.get_tile_image_by_gid(gid)
                if imagem is None:
                    continue

                x_scaled = objeto.x * SCALE_FACTOR
                y_scaled = objeto.y * SCALE_FACTOR

                Item((x_scaled, y_scaled), imagem, nome, self.all_sprites, self.grupo_items)
                if nome == 'shield':
                    self.total_shields += 1
            
    def jogador_vivo (self):
        self.jogador.vidas -= 1
        
        if self.jogador.vidas <= 0:
            self.inventario.clear()
            return 'GAMEOVER'
        else:
            self.jogador.rect.topleft = self.spawn_point
            self.jogador.reset_state() 
            self.alternar_gravidade(force_state=self.gravidade_invertida)
            
            return 'JOGO'
            
    def alternar_gravidade(self, force_state=None):
        if force_state is None:
            self.gravidade_invertida = not self.gravidade_invertida
        else:
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
            
        if force_state is None:
            self.tempo_inicio_estado = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return 'SAIR'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.mostrar_inventario = not self.mostrar_inventario
                return None
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return 'SAIR'
        return None
            
    def update(self, dt):
        self.all_sprites.update(dt)

        if self.tempo_inicio_estado is not None:
            tempo_atual = pygame.time.get_ticks()
            if tempo_atual - self.tempo_inicio_estado >= self.intervalo_mudanca:
                self.alternar_gravidade() 
                
        estado_atual = 'JOGO'
        if self.jogador:
            
            # [LÓGICA CRÍTICA DE VITÓRIA]
            if self.final_pos and self.shields_coletados >= 5:
                if pygame.sprite.collide_rect(self.jogador, self.final_pos):
                    # 1. Calcula o tempo de conclusão
                    self.tempo_conclusao = pygame.time.get_ticks() - self.tempo_inicio_jogo
                    
                    # 2. Retorna o estado e o valor (o tempo em milissegundos)
                    return 'VITORIA', self.tempo_conclusao
                    
            if pygame.sprite.spritecollideany(self.jogador, self.grupo_agua):
                estado_atual = self.jogador_vivo()

            itens_coletados = pygame.sprite.spritecollide(self.jogador, self.grupo_items, dokill=False)
            for item in itens_coletados:
                tipo = getattr(item, 'tipo', None)
                imagem_item = item.image.copy() if hasattr(item, 'image') and item.image is not None else None

                pickup = self.assets.get('pickup_sound')
                if pickup:
                    pickup.play()

                self.inventario.append({'tipo': tipo, 'image': imagem_item})

                if tipo == 'shield':
                    self.shields_coletados += 1

                item.kill()
                
            for monstro in self.grupo_monstros:
                if not self.jogador.rect.colliderect(monstro.rect):
                    continue

                prev = getattr(self.jogador, 'prev_rect', self.jogador.rect)

                LAND_TOLERANCE = 20
                HORIZ_ALIGN_FACTOR = 1.0

                largura_rel = max(monstro.rect.width, self.jogador.rect.width)
                alinhado_horizontal = abs(self.jogador.rect.centerx - monstro.rect.centerx) <= largura_rel * HORIZ_ALIGN_FACTOR

                player_half = self.jogador.rect.copy()
                monster_half = monstro.rect.copy()

                if self.jogador.gravidade_valor > 0:
                    player_half.top = self.jogador.rect.centery
                    monster_half.bottom = monstro.rect.centery
                    moving_towards = (self.jogador.direcao.y > 0) or (prev.bottom <= monstro.rect.top + LAND_TOLERANCE)
                else:
                    player_half.bottom = self.jogador.rect.centery
                    monster_half.top = monstro.rect.centery
                    moving_towards = (self.jogador.direcao.y < 0) or (prev.top >= monstro.rect.bottom - LAND_TOLERANCE)

                if player_half.colliderect(monster_half) and moving_towards and alinhado_horizontal:
                    monstro.kill()
                    stomp = self.assets.get('stomp_sound')
                    if stomp:
                        stomp.play()
                    sinal = -1 if self.jogador.gravidade_valor < 0 else 1
                    self.jogador.direcao.y = sinal * (abs(self.jogador.velocidade_y) / 2)
                    continue

                estado_atual = self.jogador_vivo()
                break


        return estado_atual

        
    def draw(self):
        self.window.fill(COR_FUNDO)
        
        if self.jogador:
            fundo_atual = self.assets[self.fundo]
            self.all_sprites.custom_draw(self.jogador, fundo_atual)
            
            vidas_restantes = self.jogador.vidas
            texto_coracoes = chr(9829) * vidas_restantes
            img_cor = self.assets['fonte'].render(texto_coracoes, True, (255, 0, 0)) 
            self.window.blit(img_cor, (10, 10))
            
            if self.tempo_inicio_estado is not None:
                tempo_decorrido_ms = pygame.time.get_ticks() - self.tempo_inicio_estado
                tempo_restante_s = max(0, (self.intervalo_mudanca - tempo_decorrido_ms) / 1000)
                texto_tempo = f"MUDANÇA EM: {tempo_restante_s:.1f}s"
                img_tempo = self.assets['fonte'].render(texto_tempo, True, (255, 255, 255))
                
                pos_x = self.window.get_width() // 2 - img_tempo.get_width() // 2
                self.window.blit(img_tempo, (pos_x, 10))
                
            if self.mostrar_inventario:
                inv_w, inv_h = 400, 200
                inv_surf = pygame.Surface((inv_w, inv_h), pygame.SRCALPHA)
                inv_surf.fill((0, 0, 0, 180))
                inv_x = self.window.get_width()//2 - inv_w//2
                inv_y = self.window.get_height()//2 - inv_h//2
                
                titulo = self.assets['fonte2'].render('INVENTARIO', True, (255,255,255))
                inv_surf.blit(titulo, (10, 10))

                padding = 10
                thumb_size = 48
                x = padding
                y = 40
                for entry in self.inventario:
                    img = entry.get('image')
                    if isinstance(img, pygame.Surface):
                        thumb = pygame.transform.scale(img, (thumb_size, thumb_size))
                    else:
                        thumb = pygame.Surface((thumb_size, thumb_size))
                        thumb.fill((100,100,100))

                    inv_surf.blit(thumb, (x, y))
                    x += thumb_size + padding
                    if x + thumb_size + padding > inv_w:
                        x = padding
                        y += thumb_size + padding

                self.window.blit(inv_surf, (inv_x, inv_y))
            
        else:
            self.all_sprites.draw(self.window)
    
    def restart(self):
        if hasattr(self, 'all_sprites'):
            self.all_sprites.empty()

        self.collision_sprites.empty()
        self.grupo_escadas.empty()
        self.grupo_monstros.empty()
        self.grupo_agua.empty()
        self.grupo_items.empty()
        
        self.inventario.clear()
        self.total_shields = 0
        self.shields_coletados = 0

        self.tempo_inicio_estado = None
        self.gravidade_invertida = False
        self.fundo = 'fundo_mundonormal'

        # Zera variáveis do cronômetro de speedrun
        self.tempo_inicio_jogo = 0
        self.tempo_conclusao = 0

        self.setup()

        if self.jogador:
            self.jogador.vidas = self.assets.get('vidas_max', self.jogador.vidas)
            self.jogador.set_gravidade(gravidade_normal, velocidade_y)
            self.jogador.rect.topleft = self.spawn_point