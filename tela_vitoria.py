"""
Tela de vitória do jogo SWITCH BACK.

Exibe o tempo final de conclusão e uma instrução para acessar o ranking.
O jogador pode pressionar 'R' para registrar o tempo e visualizar o ranking.
"""

import pygame
from constantes import *  # PRETO, VERMELHO, AZUL, WINDOWWIDHT, WINDOWHEIGHT


class TelaVitoria:
    """Tela exibida quando o jogador vence o jogo.

    Mostra o tempo total de conclusão e permite ao jogador ir para o ranking.
    """

    def __init__(self, window, assets):
        """Inicializa a tela de vitória.

        Args:
            window (pygame.Surface): Superfície principal do jogo.
            assets (dict): Dicionário de recursos (imagens, fontes, sons, etc.).
        """
        self.window = window
        self.assets = assets
        self.tempo_final_ms = 0
        self.nome_jogador = ""

    def set_tempo_final(self, tempo_ms, nome):
        """Define o tempo final e o nome do jogador para exibição.

        Args:
            tempo_ms (int): Tempo final do jogador em milissegundos.
            nome (str): Nome do jogador.
        """
        self.tempo_final_ms = tempo_ms
        self.nome_jogador = nome

    def handle_event(self, event):
        """Processa eventos de teclado na tela de vitória.

        Tecla:
            - R: vai para o ranking, enviando o nome e o tempo do jogador.

        Args:
            event (pygame.event.Event): Evento Pygame de teclado.

        Returns:
            tuple[str, dict] | None:  
                ('RANKING', {'nome': ..., 'tempo_ms': ...}) se o jogador pressionar R,  
                None se nenhuma ação for detectada.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                payload = {'nome': self.nome_jogador, 'tempo_ms': self.tempo_final_ms}
                return 'RANKING', payload
        return None

    def update(self, dt):
        """Atualiza o estado da tela (sem lógica dinâmica).

        Args:
            dt (float): Delta time em segundos.

        Returns:
            str: 'VITORIA' (identificador da tela).
        """
        return 'VITORIA'

    def draw(self):
        """Desenha o fundo, o tempo final e a instrução para o jogador."""
        self.window.fill(PRETO)
        self.window.blit(self.assets['tela_vitoria'], (0, 0))

        # Tempo formatado (MM:SS:CC)
        total_segundos = self.tempo_final_ms // 1000
        ms = self.tempo_final_ms % 1000
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        tempo_formatado = f"{minutos:02}:{segundos:02}:{ms//10:02}"

        texto_tempo = f"TEMPO: {tempo_formatado}"
        img_tempo = self.assets['fonte2'].render(texto_tempo, True, (0, 255, 0))
        rect_tempo = img_tempo.get_rect(center=(WINDOWWIDHT // 2, WINDOWHEIGHT - 100))
        self.window.blit(img_tempo, rect_tempo)

        # Instrução
        texto_instrucao = "PRESSIONE R PARA ACESSAR O RANKING"
        img_instrucao = self.assets['fonte2'].render(texto_instrucao, True, (255, 255, 255))
        rect_instrucao = img_instrucao.get_rect(center=(WINDOWWIDHT // 2, WINDOWHEIGHT - 50))
        self.window.blit(img_instrucao, rect_instrucao)
