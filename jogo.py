import pygame
from tela_inicio import TelaInicio
from tela_jogo import TelaJogo
from tela_vitoria import TelaVitoria
from tela_gameover import TelaGameOver
from tela_input_nome import TelaInputNome 
from tela_ranking import TelaRanking 
from tela_instrucoes_1 import TelaInstrucoes1
from tela_instrucoes_2 import TelaInstrucoes2 
from constantes import *
import os

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
    assets['tela_nome'] = pygame.transform.scale(pygame.image.load('assets/tela_nome.png'), (1600,880))
    assets['game_over'] = pygame.transform.scale(pygame.image.load('assets/game_over.png'), (1600,880))
    assets['tela_vitoria'] = pygame.transform.scale(pygame.image.load('assets/tela_vitoria.png'), (1600,880))
    assets['tela_instrucoes1'] = pygame.transform.scale(pygame.image.load('assets/tela_instrucoes1.png'), (1600,880))
    assets['tela_instrucoes2'] = pygame.transform.scale(pygame.image.load('assets/tela_instrucoes2.png'), (1600,880))

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
    # carrega sons de efeitos
    caminho_pickup = os.path.join('assets', 'sound', 'capturaitem.mp3')
    if os.path.exists(caminho_pickup):
        assets['pickup_sound'] = pygame.mixer.Sound(caminho_pickup)
    else:
        assets['pickup_sound'] = None
    
    # carrega som de passos
    caminho_passos = os.path.join('assets', 'sound', 'passo.mp3')
    if os.path.exists(caminho_passos):
        assets['footstep_sound'] = pygame.mixer.Sound(caminho_passos)
        assets['footstep_sound'].set_volume(0.3)  # volume mais baixo para passos
    else:
        assets['footstep_sound'] = None

    # carrega som de pisada em monstro
    caminho_pisada = os.path.join('assets', 'sound', 'pisando.mp3')
    if os.path.exists(caminho_pisada):
        assets['stomp_sound'] = pygame.mixer.Sound(caminho_pisada)
    else:
        assets['stomp_sound'] = None

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

        self.nome_jogador = "" # Variável para armazenar o nome
        
        # Carrega e inicia a musica de fundo
        caminho_musica = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sound', 'matue.mp3')
        self.theme_music_path = caminho_musica if os.path.exists(caminho_musica) else None
        if self.theme_music_path:
            pygame.mixer.music.load(self.theme_music_path)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)

        self.telas = {
            'INPUT_NOME': TelaInputNome(self.window, self.assets),
            'INICIO': TelaInicio(self.window,self.assets),
            'JOGO': TelaJogo(self.window, self.assets),
            'VITORIA': TelaVitoria(self.window, self.assets),
            'GAMEOVER': TelaGameOver(self.window,self.assets),
            'RANKING': TelaRanking(self.window, self.assets),
            'INSTRUCOES1': TelaInstrucoes1(self.window, self.assets),
            'INSTRUCOES2': TelaInstrucoes2(self.window, self.assets)
        }

        # define a tela inicial
        self.tela_atual = 'INICIO'
        # carrega caminho de musicas de gameover (opcional)
        self.gameover_music_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'sound', 'gameovertheme.mp3')
        
    # loop principal
    def run(self):
        while self.rodando:
            dt = self.clock.tick(60) / 1000.0

            # variaveis de controle
            proximo_estado = None
            tempo_final_ms = None
            
            # processa 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.rodando = False
                    continue
                
                # passa eventos para a tela atual
                tela_ativa = self.telas[self.tela_atual]
                if hasattr(tela_ativa, 'handle_event'):
                    resultado_evento = tela_ativa.handle_event(event)

                    # desempacota o resultado do evento (pode ser tupla ou string)
                    valor_retornado = None
                    if isinstance(resultado_evento, tuple) and len(resultado_evento) == 2:
                        proximo_estado, valor_retornado = resultado_evento
                    elif isinstance(resultado_evento, str):
                        proximo_estado = resultado_evento

                    if proximo_estado == 'SAIR':
                        self.rodando = False
                        continue
                        
                    if proximo_estado == 'RESTART':
                        # Se for RESTART, executamos a ação de reinício
                        if hasattr(self.telas['JOGO'], 'restart'):
                            self.telas['JOGO'].restart()
                        else:
                            self.telas['JOGO'].setup()
                        
                        self.telas['JOGO'].iniciar_tempo_gravidade()
                        self.tela_atual = 'JOGO'
                        self._handle_screen_music(self.tela_atual)
                        
                        proximo_estado = None 
                        break 

                    if self.tela_atual == 'INPUT_NOME' and valor_retornado:
                        self.nome_jogador = valor_retornado
                        # Força a transição para JOGO
                        proximo_estado = 'INSTRUCOES1' 
                        
            # 2. atualiza tela
            tela_ativa = self.telas[self.tela_atual]
            resultado_update = tela_ativa.update(dt)

            # desempacota o resultado do update (vindo tipicamente de TelaJogo)
            proximo_estado_update = None
            if isinstance(resultado_update, tuple) and len(resultado_update) == 2:
                proximo_estado_update, tempo_final_ms = resultado_update
                
                # se a TelaJogo retornou o estado final e o tempo
                if proximo_estado_update in ['VITORIA', 'GAMEOVER'] and self.tela_atual == 'JOGO':
                    proximo_estado = proximo_estado_update
                
            elif isinstance(resultado_update, str):
                # filtra comandos de acao como 'RESTART'
                if resultado_update == 'RESTART': 
                    proximo_estado = None 
                elif resultado_update != self.tela_atual:
                    proximo_estado = resultado_update


            # troca de tela e processa o resultado final (TEMPO)
            if proximo_estado and proximo_estado != self.tela_atual:

                # se for para VITORIA, salva o ranking ANTES de mudar de tela
                if proximo_estado == 'VITORIA' and tempo_final_ms is not None:
                    self.telas['VITORIA'].set_tempo_final(tempo_final_ms, self.nome_jogador)

                # se for para JOGO (inicio de um novo jogo ou vindo do menu), reinicia o nível e a gravidade.
                if proximo_estado == 'JOGO':
                    # chama restart() para garantir que o mapa e objetivos sejam zerados
                    if hasattr(self.telas['JOGO'], 'restart'):
                         self.telas['JOGO'].restart() 
                    
                    self.telas['JOGO'].iniciar_tempo_gravidade() # inicia o timer e cronômetro
                    
                self.tela_atual = proximo_estado
                self._handle_screen_music(self.tela_atual)

            # desenha a tela atual
            if hasattr(tela_ativa, 'draw'):
                tela_ativa.draw()
                
            pygame.display.update()
    
        pygame.quit() 

    def _handle_screen_music(self, screen_name):
        # troca a música quando for para GAMEOVER (toca gameover) ou restaura o tema
        if screen_name == 'GAMEOVER' and os.path.exists(self.gameover_music_path):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.gameover_music_path)
            pygame.mixer.music.play(-1)
            return

        if self.theme_music_path:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.theme_music_path)
            pygame.mixer.music.play(-1)
            
if __name__ == '__main__':
    game = Jogo()
    game.run()