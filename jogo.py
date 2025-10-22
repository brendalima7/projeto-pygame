from tela_inicio import TelaInicio
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
            image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (50,50))
            frames.append(image)
        animacoes[direction] = frames
    return animacoes

def condicoes_iniciais():  
    assets = {} 
    assets['jogador_mapa'] = pygame.transform.scale(pygame.image.load('assets/jogador_mapa/down/0.png').convert_alpha(), (100,100))
    assets['fundo_mundonormal'] = pygame.transform.scale(pygame.image.load('assets/fundo_mundonormal.png'), (3200,1600))
    assets['fundo_mundoinvertido'] = pygame.transform.scale(pygame.image.load('assets/fundo_mundoinvertido.png'), (3200,1600))
    assets['fonte'] = pygame.font.Font('assets/font/PressStart2P.ttf', 28)
    assets['fonte2'] = pygame.font.Font('assets/font/PressStart2P.ttf', 24)
    assets['fundo_inicial']=pygame.transform.scale(pygame.image.load('assets/fundo_inicial.png'), (1600,880))
    assets['game_over1'] = pygame.transform.scale(pygame.image.load('assets/game_over1.png'), (1920,980))
    assets['game_over2'] = pygame.transform.scale(pygame.image.load('assets/game_over2.png'), (1920,980))

    # imagens de animacao jogador
    assets['animacoes_jogador'] = carrega_frames_animacao(
        arquivo_base='assets/jogador_mapa',
        direcoes=['down', 'up', 'left', 'right'],
        num_frames=4
    )
    # imagens de animacao monstro
    assets['animacoes_monstro'] = carrega_frames_animacao(
        arquivo_base='assets/jogador_mapa', 
        direcoes=['left', 'right'],        
        num_frames=4                      
    ) 
    assets['vidas_max'] = 5
    return assets

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.window = pygame.display.set_mode((WINDOWWIDHT, WINDOWHEIGHT))
        pygame.display.set_caption('SWITCH BACK')
        
        self.clock = pygame.time.Clock()
        self.rodando = True 

        self.assets = condicoes_iniciais()

        # Carrega e inicia a música de fundo
        caminho_musica = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sound', 'theme.mp3')
        if os.path.exists(caminho_musica):
            pygame.mixer.music.load(caminho_musica)
            pygame.mixer.music.set_volume(0.5)  # Ajusta o volume para 50%
            pygame.mixer.music.play(-1)  # -1 faz a música tocar em loop infinito

        self.telas = {
            'INICIO': TelaInicio(self.window,self.assets),
            'JOGO': TelaJogo(self.window, self.assets),
            'VITORIA': TelaVitoria(self.window),
            'GAMEOVER': TelaGameOver(self.window,self.assets)
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

                    # Tratamento especial para RESTART vindo da TelaGameOver
                    if resultado == 'RESTART':
                        # faz hard restart do nível e volta para a tela de jogo
                        # garante que TelaJogo possui restart()
                        if hasattr(self.telas['JOGO'], 'restart'):
                            self.telas['JOGO'].restart()
                        else:
                            # fallback para recriar via setup() caso não exista restart()
                            self.telas['JOGO'].setup()
                        # iniciar o timer de gravidade e alternar para JOGO
                        self.telas['JOGO'].iniciar_tempo_gravidade()
                        self.tela_atual = 'JOGO'
                        # pula tratamento normal abaixo
                        continue

                    if resultado == 'SAIR':
                        self.rodando = False
                    elif resultado and resultado in self.telas:
                        # se for voltar para JOGO via outra tela (ex: INICIO -> JOGO)
                        if resultado == 'JOGO':
                            self.telas['JOGO'].iniciar_tempo_gravidade()
                        self.tela_atual = resultado

            # atualiza a tela atual
            tela_ativa = self.telas[self.tela_atual]
            proximo_estado = tela_ativa.update(dt)

            # troca de tela se necessário
            if proximo_estado and proximo_estado != self.tela_atual:

             # se o próximo estado for 'JOGO', inicia o tempo da gravidade.
                if proximo_estado == 'JOGO':
                    self.telas['JOGO'].iniciar_tempo_gravidade()
                self.tela_atual = proximo_estado

            # desenha a tela atual
            if hasattr(tela_ativa, 'draw'):
                tela_ativa.draw()
            
            pygame.display.update()
 
        pygame.quit() 
            
if __name__ == '__main__':
    game = Jogo()
    game.run()