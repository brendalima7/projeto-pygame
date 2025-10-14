import pygame
from tela_inicio import TelaInicio
from tela_mapa import TelaMapa
from tela_jogo import TelaJogo
from tela_vitoria import TelaVitoria
from tela_gameover import TelaGameOver
import constantes 

tela_atual = 'INICIO' 

def condicoes_iniciais(): 
    assets = {}
    assets['jogador'] = pygame.image.load('assets/player.png').convert_alpha()
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
            self.clock.tick(60) 
            
            tela_ativa = self.telas[self.tela_atual]
            
            # atualizacao da tela ativa
            proximo_estado = tela_ativa.update()

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