from sprites import *
from cameras import *
from constantes import *

class TelaJogo:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets

        # grupos - usando CameraGroup para seguir o jogador
        self.all_sprites = CameraGroup(5000, 2500)
        self.collision_sprites = pygame.sprite.Group()
        
        self.jogador = None

        # load game
        self.setup()

    def setup(self):
        tmx_mapa = load_pygame(join('data', 'mapa_teste.tmx'))
        for x, y, imagem in tmx_mapa.get_layer_by_name('Principal').tiles():
            # instancia a classe Sprite para criar os blocos
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, (self.all_sprites, self.collision_sprites))  
        for x, y, imagem in tmx_mapa.get_layer_by_name('Decoracao2').tiles():
            # instancia a classe Sprite para criar a decoracao
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, self.all_sprites) 
        for objeto in tmx_mapa.get_layer_by_name('Entities'):
            if objeto.name == 'Player':
                # instancia a classe Jogador para criar o jogador na posicao do Entities determinada
                self.jogador = Jogador(self.window, self.assets, (objeto.x, objeto.y), self.all_sprites, self.collision_sprites)
        for x, y, imagem in tmx_mapa.get_layer_by_name('Agua').tiles():
            # instancia a classe Sprite para criar os blocos
            Sprite((x*TILE_SIZE, y*TILE_SIZE), imagem, (self.all_sprites, self.collision_sprites)) 
        
  
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
        return 'JOGO'
    
    def draw(self):
        self.window.fill(COR_FUNDO)
        # usa custom_draw com a câmera seguindo o jogador
        if self.jogador:
            self.all_sprites.custom_draw(self.jogador, self.assets['fundo_mundonormal'])
        else:
            # fallback caso o jogador não exista ainda
            self.all_sprites.draw(self.window)