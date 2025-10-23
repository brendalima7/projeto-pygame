"""
Contém a definição da classe `Jogo`, funções utilitárias para carregar
assets/frames e a rotina principal (`run`) que gerencia o loop do jogo
e a troca entre telas.
"""

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
# Importação corrigida para evitar circular dependency e usar a função de caminho
from utils import resource_path

# 2. FUNÇÃO UTILITÁRIA CORRIGIDA: AGORA USA resource_path INTERNAMENTE
def carrega_frames_animacao(arquivo_base_relativo, direcoes, num_frames):
    """Carrega e escala frames de animação a partir de um diretório.
    
    A função foi modificada para usar resource_path no caminho completo do arquivo.

    Args:
        arquivo_base_relativo (str): Caminho base onde estão as pastas de direção (ex: 'assets/jogador_mapa').
        direcoes (list[str]): Lista de nomes de subpastas (direções).
        num_frames (int): Número de frames a carregar por direção.

    Returns:
        dict: Dicionário onde cada chave é uma direção e o valor é a lista
              de superfícies Pygame (frames) escaladas.
    """
    animacoes = {}
    
    # A base do path deve ser obtida aqui dentro da função, antes do loop
    base_path_abs = resource_path(arquivo_base_relativo)
    
    for direction in direcoes:
        frames = []
        path = os.path.join(base_path_abs, direction) # Agora usa a base ABSOLUTA
        
        for i in range(num_frames):
            filename = f"{i}.png" 
            full_path = os.path.join(path, filename)
            
            # O caminho 'full_path' já é compatível com PyInstaller
            image = pygame.transform.scale(pygame.image.load(full_path).convert_alpha(), (50,50))
            frames.append(image)
            
        animacoes[direction] = frames
    return animacoes


# 3. FUNÇÃO DE CARREGAMENTO DE ASSETS CORRIGIDA
def condicoes_iniciais():
    """Carrega e retorna um dicionário com assets iniciais utilizados pelo jogo.
    
    Todos os caminhos de assets foram corrigidos para usar resource_path().

    Returns:
        dict: Dicionário `assets` contendo superfícies, fontes, sons e
              configurações (ex: 'vidas_max').
    """
    assets = {}
    
    # --- IMAGENS ---
    caminho_jogador = resource_path(os.path.join('assets', 'jogador_mapa', 'down', '0.png'))
    assets['jogador_mapa'] = pygame.transform.scale(pygame.image.load(caminho_jogador).convert_alpha(), (100,100))
    
    caminho_normal = resource_path(os.path.join('assets', 'fundo_mundonormal.png'))
    assets['fundo_mundonormal'] = pygame.transform.scale(pygame.image.load(caminho_normal), (3200,1600))
    
    caminho_invertido = resource_path(os.path.join('assets', 'fundo_mundoinvertido.png'))
    assets['fundo_mundoinvertido'] = pygame.transform.scale(pygame.image.load(caminho_invertido), (3200,1600))
    
    caminho_inicial = resource_path(os.path.join('assets', 'fundo_inicial.png'))
    assets['fundo_inicial']=pygame.transform.scale(pygame.image.load(caminho_inicial), (1600,880))
    
    caminho_nome = resource_path(os.path.join('assets', 'tela_nome.png'))
    assets['tela_nome'] = pygame.transform.scale(pygame.image.load(caminho_nome), (1600,880))
    
    caminho_go = resource_path(os.path.join('assets', 'game_over.png'))
    assets['game_over'] = pygame.transform.scale(pygame.image.load(caminho_go), (1600,880))
    
    caminho_vitoria = resource_path(os.path.join('assets', 'tela_vitoria.png'))
    assets['tela_vitoria'] = pygame.transform.scale(pygame.image.load(caminho_vitoria), (1600,880))
    
    caminho_ins1 = resource_path(os.path.join('assets', 'tela_instrucoes1.png'))
    assets['tela_instrucoes1'] = pygame.transform.scale(pygame.image.load(caminho_ins1), (1600,880))
    
    caminho_ins2 = resource_path(os.path.join('assets', 'tela_instrucoes2.png'))
    assets['tela_instrucoes2'] = pygame.transform.scale(pygame.image.load(caminho_ins2), (1600,880))
    
    # --- FONTES ---
    caminho_fonte = resource_path(os.path.join('assets', 'font', 'PressStart2P.ttf'))
    assets['fonte'] = pygame.font.Font(caminho_fonte, 28)
    assets['fonte2'] = pygame.font.Font(caminho_fonte, 24)
    
    # --- ANIMAÇÕES ---
    
    assets['animacoes_jogador'] = carrega_frames_animacao(
        arquivo_base_relativo='assets/jogador_mapa',
        direcoes=['down', 'up', 'left', 'right'],
        num_frames=4
    )
    
    assets['animacoes_monstro'] = carrega_frames_animacao(
        arquivo_base_relativo='assets/jogador_mapa', 
        direcoes=['left', 'right'], 
        num_frames=4 
    ) 
    assets['vidas_max'] = 5
    
    # --- SONS ---
    
    caminho_pickup_abs = resource_path(os.path.join('assets', 'sound', 'capturaitem.mp3'))
    if os.path.exists(caminho_pickup_abs):
        assets['pickup_sound'] = pygame.mixer.Sound(caminho_pickup_abs)
    else:
        assets['pickup_sound'] = None
    
    caminho_passos_abs = resource_path(os.path.join('assets', 'sound', 'passo.mp3'))
    if os.path.exists(caminho_passos_abs):
        assets['footstep_sound'] = pygame.mixer.Sound(caminho_passos_abs)
        assets['footstep_sound'].set_volume(0.3)
    else:
        assets['footstep_sound'] = None

    caminho_pisada_abs = resource_path(os.path.join('assets', 'sound', 'pisando.mp3'))
    if os.path.exists(caminho_pisada_abs):
        assets['stomp_sound'] = pygame.mixer.Sound(caminho_pisada_abs)
    else:
        assets['stomp_sound'] = None

    return assets

class Jogo:
    """Classe que encapsula o loop principal do jogo e o gerenciamento de telas.
    """

    def __init__(self):
        """Inicializa Pygame, carrega assets, telas e configurações iniciais."""
        pygame.init()
        pygame.mixer.init()
        
        self.window = pygame.display.set_mode((WINDOWWIDHT, WINDOWHEIGHT))
        pygame.display.set_caption('SWITCH BACK')
        
        self.clock = pygame.time.Clock()
        self.rodando = True 

        self.assets = condicoes_iniciais()

        self.nome_jogador = "" # Variável para armazenar o nome
        
        # CORREÇÃO: Usar resource_path para caminhos de música
        caminho_musica = resource_path(os.path.join('assets', 'sound', 'matue.mp3'))
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
        
        # CORREÇÃO: Usar resource_path para caminhos de música (Game Over e Vitória)
        self.gameover_music_path = resource_path(os.path.join('assets', 'sound', 'gameovertheme.mp3'))
        self.vitoria_music_path = resource_path(os.path.join('assets', 'sound', 'vitoria_sound.mp3'))
        
        self.current_music_path = None
        
    def run(self):
        """Executa o loop principal do jogo.
        """
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
                        
            # atualiza
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
        """Toca a música apropriada para a tela ativa.

        Prioridade:
            1. GAMEOVER -> gameover_music_path
            2. VITORIA  -> vitoria_music_path
            3. padrão   -> theme_music_path

        A função evita recarregar a mesma faixa repetidamente verificando
        `self.current_music_path`.
        
        Args:
            screen_name (str): Identificador da tela (ex: 'GAMEOVER', 'VITORIA', ...).
        """
        # GAMEOVER
        if screen_name == 'GAMEOVER' and os.path.exists(self.gameover_music_path):
            if self.current_music_path != self.gameover_music_path:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.gameover_music_path)
                pygame.mixer.music.play(-1)
                self.current_music_path = self.gameover_music_path
            return

        # VITORIA
        if screen_name == 'VITORIA' and os.path.exists(self.vitoria_music_path):
            if self.current_music_path != self.vitoria_music_path:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.vitoria_music_path)
                pygame.mixer.music.play(-1)
                self.current_music_path = self.vitoria_music_path
            return

        # TEMA PADRAO
        if self.theme_music_path and os.path.exists(self.theme_music_path):
            if self.current_music_path != self.theme_music_path:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(self.theme_music_path)
                pygame.mixer.music.play(-1)
                self.current_music_path = self.theme_music_path


if __name__ == '__main__':
    game = Jogo()
    game.run()