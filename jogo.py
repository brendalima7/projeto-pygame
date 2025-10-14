import pygame
from tela_inicio import TelaInicio
from tela_mapa import TelaMapa
from tela_jogo import TelaJogo
from tela_vitoria import TelaVitoria
from tela_gameover import TelaGameOver

tela_atual = 'INICIO'

def condicoes_iniciais(): 
    assets = {}
    # jogador
    assets['jogador'] = pygame.image.load('assets/player.png').convert_alpha()
    return assets

class Jogo:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.WINDOWWIDHT = info.current_w
        self.WINDOWHEIGHT = info.current_h

        self.window = pygame.display.set_mode((self.WINDOWWIDHT, self.WINDOWHEIGHT))
        pygame.display.set_caption('SWITCH BACK')

        self.assets = condicoes_iniciais()
        self.telajogo = TelaJogo(self.window, self.assets)

        # controle de telas
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
            tela_ativa = self.telas[self.tela_atual]
            proximo_estado = tela_ativa.update()

            # verificação de saída
            if proximo_estado == 'SAIR':
                rodando = False

            elif proximo_estado != self.tela_atual:
                self.tela_atual = proximo_estado

            tela_ativa.draw()
            
            pygame.display.update() 

        pygame.quit() 
            
if __name__ == '__main__':
    game = Jogo()
    game.run()