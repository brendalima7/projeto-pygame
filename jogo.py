import pygame
from tela_inicio import TelaInicio
from tela_mapa import TelaMapa
from tela_jogo import TelaJogo
from tela_vitoria import TelaVitoria
from tela_gameover import TelaGameOver
import constantes 
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
            image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha() , (100,100))
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

    # atribui as imagens de animacao 
    assets['animacoes_jogador'] = carrega_frames_animacao(
        arquivo_base = 'assets\jogador_mapa',
        direcoes=['down', 'up', 'left', 'right'],
        num_frames = 4
    )
    return assets

class Jogo:
    def __init__(self):
        pygame.init() 
        
        self.WINDOWWIDHT = constantes.WINDOWWIDHT
        self.WINDOWHEIGHT = constantes.WINDOWHEIGHT
        self.window = pygame.display.set_mode((self.WINDOWWIDHT, self.WINDOWHEIGHT), pygame.FULLSCREEN)
        pygame.display.set_caption('SWITCH BACK')
        
        self.assets = condicoes_iniciais()
        self.clock = pygame.time.Clock() # cria o relogio para controle de FPS

        self.telas = {
            'INICIO': TelaInicio(self.window),
            'MAPA': TelaMapa(self.window, self.assets),
            'JOGO': TelaJogo(self.window, self.assets),
            'VITORIA': TelaVitoria(self.window),
            'GAMEOVER': TelaGameOver(self.window)
        }
        self.tela_atual = tela_atual

    # loop principal
    def run(self):
        rodando = True 
        while rodando:
            # controle de FPS
            dt = self.clock.tick(60)/1000.0
            
            tela_ativa = self.telas[self.tela_atual]
            
            # atualizacao da tela ativa
            proximo_estado = tela_ativa.update(dt)

            # verifica transicao de tela
            if proximo_estado == 'SAIR':
                rodando = False

            elif proximo_estado != self.tela_atual:
                self.tela_atual = proximo_estado

            # desenha
            tela_ativa.draw()
            
            # atualizacao 
            pygame.display.flip()

        pygame.quit() 
            
if __name__ == '__main__':
    game = Jogo()
    game.run()