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
        # NOVO: Grupo para detecção da água
        self.grupo_agua = pygame.sprite.Group()

        # load game
        self.setup()

    def setup(self):
        tmx_mapa = load_pygame(join('data', 'mapa_teste.tmx'))

        map_pixel_width = tmx_mapa.width * TILE_SIZE
        map_pixel_height = tmx_mapa.height * TILE_SIZE
        
        self.all_sprites = CameraGroup(map_pixel_width, map_pixel_height)

        for x, y, imagem in tmx_mapa.get_layer_by_name('Principal').tiles():
            # instancia a classe Sprite para criar os blocos
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, (self.all_sprites, self.collision_sprites))  
        for x, y, imagem in tmx_mapa.get_layer_by_name('Decoracao2').tiles():
            # instancia a classe Sprite para criar a decoracao
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, self.all_sprites) 
        for objeto in tmx_mapa.get_layer_by_name('Entities'):
            if objeto.name == 'Player':
                player_pos = (objeto.x * SCALE_FACTOR , objeto.y * SCALE_FACTOR)
                self.spawn_point = player_pos
                # instancia a classe Jogador para criar o jogador na posicao do Entities determinada
                self.jogador = Jogador(
                    self.window, self.assets, player_pos, # Apenas a posição
                    self.all_sprites, self.collision_sprites,
                    map_pixel_width, map_pixel_height, 
                    self.grupo_escadas
                    )

        for x, y, imagem in tmx_mapa.get_layer_by_name('Agua').tiles():
            # instancia a classe Sprite para criar os blocos
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, (self.all_sprites, self.grupo_agua))

        for x, y, imagem in tmx_mapa.get_layer_by_name('Escada').tiles():
            # instancia a classe Sprite para criar os blocos
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
            return 'JOGO'
        
    def handle_event(self, event):
        # transicoes de tela
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

        # checa colisão com a água
        if self.jogador:
            if pygame.sprite.spritecollideany(self.jogador, self.grupo_agua):
                return self.jogador_vivo()
        return 'JOGO'
    
    def draw(self):
        self.window.fill(COR_FUNDO)
    
        # usa custom_draw com a câmera seguindo o jogador
        if self.jogador:
            self.all_sprites.custom_draw(self.jogador, self.assets['fundo_mundonormal'])
            
            # CORREÇÃO: Usa self.jogador.vidas para desenhar os corações
            vidas_restantes = self.jogador.vidas
            texto_coracoes = chr(9829) * vidas_restantes
            
            # Usa a fonte carregada
            img_cor = self.assets['fonte'].render(texto_coracoes, True, (255, 0, 0)) # COR VERMELHA
            
            # Posição fixa na janela (HUD), por exemplo, (10, 10) para uma margem
            self.window.blit(img_cor, (10, 10))
        else:
            # fallback caso o jogador não exista ainda
            self.all_sprites.draw(self.window)