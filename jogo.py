import pygame
from tela_jogo import TelaJogo

tela_atual = 'JOGO'

def condicoes_iniciais(): 
    assets = {}
    # jogador
    assets['jogador'] = pygame.transform.scale(pygame.image.load('assets/ball.png'), (50,50))
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
            'JOGO': TelaJogo(self.window, self.assets)
        }
        self.tela_atual = tela_atual

    # loop principal
    def run(self):
        rodando = True 
        while rodando:
            proximo_estado = self.telajogo.update()
            # verificação de saída
            if proximo_estado == 'SAIR':
                rodando = False

            self.telajogo.draw()

            pygame.display.update() 
                      
        pygame.quit() 
            
if __name__ == '__main__':
    game = Jogo()
    game.run()