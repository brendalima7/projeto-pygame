# tela_jogo.py
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
        
        self.jogador = None

        self.spawn_point = None 
        self.grupo_agua = pygame.sprite.Group()

        # NOVO: Variáveis para o ciclo de gravidade
        self.gravidade_invertida = False
        self.tempo_inicio_estado = pygame.time.get_ticks() 
        self.intervalo_mudanca = tempo_mudanca_gravidade # Definido em constantes.py
        
        # NOVO: Variável para rastrear a chave da imagem de fundo atual
        self.fundo = 'fundo_mundonormal'
        
        # load game
        self.setup()
        
        # Garante que o jogador já está com a gravidade e pulo iniciais
        if self.jogador:
            self.jogador.set_gravidade(gravidade_normal, velocidade_y)

    def setup(self):
        tmx_mapa = load_pygame(join('data', 'mapa_teste.tmx'))

        map_pixel_width = tmx_mapa.width * TILE_SIZE
        map_pixel_height = tmx_mapa.height * TILE_SIZE
        
        self.all_sprites = CameraGroup(map_pixel_width, map_pixel_height)

        for x, y, imagem in tmx_mapa.get_layer_by_name('Principal').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, (self.all_sprites, self.collision_sprites))
        for x, y, imagem in tmx_mapa.get_layer_by_name('Decoracao2').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, self.all_sprites) 
            
        for objeto in tmx_mapa.get_layer_by_name('Entities'):
            if objeto.name == 'Player':
                player_pos = (objeto.x * SCALE_FACTOR , objeto.y * SCALE_FACTOR)
                self.spawn_point = player_pos
                self.jogador = Jogador(
                    self.window, self.assets, player_pos,
                    self.all_sprites, self.collision_sprites,
                    map_pixel_width, map_pixel_height, 
                    self.grupo_escadas
                    )

        for x, y, imagem in tmx_mapa.get_layer_by_name('Agua').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, (self.all_sprites, self.grupo_agua))

        for x, y, imagem in tmx_mapa.get_layer_by_name('Escada').tiles():
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, self.all_sprites, self.grupo_escadas) 
            
    def jogador_vivo (self):
        self.jogador.vidas -= 1
        
        if self.jogador.vidas <= 0:
            return 'GAMEOVER'
        else:
            # Reseta a posição do jogador para o ponto de spawn
            self.jogador.rect.topleft = self.spawn_point
            # Reseta o estado (velocidade, subindo escada, etc.)
            self.jogador.reset_state() 
            # Garante que a gravidade é resetada para o estado atual do jogo após o respawn
            self.alternar_gravidade(force_state=self.gravidade_invertida) # Força o estado da gravidade atual
            return 'JOGO'
            
    # NOVO MÉTODO: Controla a alternância de gravidade e fundo
    def alternar_gravidade(self, force_state=None):
        """Alterna a gravidade, a velocidade de pulo do jogador e a imagem de fundo.
           Pode forçar um estado específico com `force_state`."""
        
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
            
        # Reseta o timer APENAS se não for um respawn forçado
        if force_state is None:
            self.tempo_inicio_estado = pygame.time.get_ticks()

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return 'SAIR'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return 'SAIR'
            if event.key == pygame.K_a:
                return 'GAMEOVER' 
            if event.key == pygame.K_v:
                return 'VITORIA' 
        return None
                
    def update(self, dt):
        self.all_sprites.update(dt)

        # NOVO: Checagem do Timer para alternar gravidade
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_inicio_estado >= self.intervalo_mudanca:
            self.alternar_gravidade() # Alterna sem forçar estado
            
        # checa colisão com a água
        if self.jogador:
            if pygame.sprite.spritecollideany(self.jogador, self.grupo_agua):
                return self.jogador_vivo()
        return 'JOGO'
    
    def draw(self):
        self.window.fill(COR_FUNDO)
    
        # usa custom_draw com a câmera seguindo o jogador
        if self.jogador:
            # NOVO: Pega a imagem de fundo correta do assets e passa para o custom_draw
            fundo_atual = self.assets[self.fundo]
            self.all_sprites.custom_draw(self.jogador, fundo_atual)
            
            # desenha vidas (coração)
            vidas_restantes = self.jogador.vidas
            texto_coracoes = chr(9829) * vidas_restantes
            img_cor = self.assets['fonte'].render(texto_coracoes, True, (255, 0, 0)) 
            self.window.blit(img_cor, (10, 10))
            
            # NOVO: Desenho do Timer
            tempo_decorrido_ms = pygame.time.get_ticks() - self.tempo_inicio_estado
            tempo_restante_s = max(0, (self.intervalo_mudanca - tempo_decorrido_ms) / 1000)
            texto_tempo = f"MUDANÇA EM: {tempo_restante_s:.1f}s"
            img_tempo = self.assets['fonte'].render(texto_tempo, True, (255, 255, 255))
            
            # posição do texto tempo
            pos_x = self.window.get_width() // 2 - img_tempo.get_width() // 2
            self.window.blit(img_tempo, (pos_x, 10))
            
        else:
            self.all_sprites.draw(self.window)