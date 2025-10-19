from tela_inicio import TelaInicio
from tela_mapa import TelaMapa
from tela_jogo import TelaJogo
from tela_vitoria import TelaVitoria
from tela_gameover import TelaGameOver
from constantes import *
import os

tela_atual = 'INICIO' 

# carrega os frames de animacao
def carrega_frames_animacao(arquivo_base, direcoes, num_frames):
    animacoes = {}
    for direction in direcoes:
        frames = []
        path = os.path.join(arquivo_base, direction)
        for i in range(num_frames):
            filename = f"{i}.png" 
            full_path = os.path.join(path, filename)
            image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (100,100))
            frames.append(image)
        animacoes[direction] = frames
    return animacoes

def condicoes_iniciais(): 
    assets = {} 
    assets['jogador_mapa'] = pygame.transform.scale(pygame.image.load('assets/jogador_mapa/down/0.png').convert_alpha(), (100,100))
    assets['map_surface'] = pygame.image.load('assets/ground.png').convert_alpha()
    assets['fundo_mundonormal'] = pygame.transform.scale(pygame.image.load('assets/fundo_mundonormal.png'), (5000,2500))
    assets['fundo_mundoinvertido'] = pygame.transform.scale(pygame.image.load('assets/fundo_mundoinvertido.png'), (5000,2500))
    assets['mapa_do_jogo'] = pygame.transform.scale(pygame.image.load('assets/mapa_normal_colisao.png'),(5000,2500))
    assets['mapa_jogo_decoracao'] = pygame.transform.scale(pygame.image.load('assets/mapa_jogo_decoracao.png'),(5000,2500))
    assets['mapa_jogo_escada'] = pygame.transform.scale(pygame.image.load('assets/mapa_jogo_escada.png'),(5000,2500))

    # imagens de animacao 
    assets['animacoes_jogador'] = carrega_frames_animacao(
        arquivo_base='assets/jogador_mapa',
        direcoes=['down', 'up', 'left', 'right'],
        num_frames=4
    )
    return assets

class Jogo:
    def __init__(self):
        pygame.init() 
        
        self.window = pygame.display.set_mode((WINDOWWIDHT, WINDOWHEIGHT))
        pygame.display.set_caption('SWITCH BACK')
        
        self.clock = pygame.time.Clock()
        self.rodando = True 

        self.assets = condicoes_iniciais()
        self.telas = {
            'INICIO': TelaInicio(self.window),
            'MAPA': TelaMapa(self.window, self.assets),
            'JOGO': TelaJogo(self.window, self.assets),
            'VITORIA': TelaVitoria(self.window),
            'GAMEOVER': TelaGameOver(self.window)
        }

        # define a tela inicial
        self.tela_atual = tela_atual
        
    # loop principal
    def run(self):
        while self.rodando:
            dt = self.clock.tick(60) / 1000.0

            # processa eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                
                # passa eventos para a tela atual (se ela tiver handle_event)
                tela_ativa = self.telas[self.tela_atual]
                if hasattr(tela_ativa, 'handle_event'):
                    resultado = tela_ativa.handle_event(event)
                    if resultado == 'SAIR':
                        self.rodando = False
                    elif resultado and resultado in self.telas:
                        self.tela_atual = resultado

            # atualiza a tela atual
            tela_ativa = self.telas[self.tela_atual]
            proximo_estado = tela_ativa.update(dt)

            # troca de tela se necessário
            if proximo_estado and proximo_estado != self.tela_atual:
                self.tela_atual = proximo_estado

            # desenha a tela atual
            if hasattr(tela_ativa, 'draw'):
                tela_ativa.draw()
            
            pygame.display.update()
 
        pygame.quit() 
            
if __name__ == '__main__':
    game = Jogo()
    game.run()