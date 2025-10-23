"""
Tela de Game Over.

Define a tela exibida quando o jogador perde. Trata entrada do usuário
para sair, reiniciar ou acessar o ranking, e desenha a tela com instruções.
"""

import pygame


class TelaGameOver:
    """Representa a tela de Game Over do jogo.

    A tela mostra a imagem de game over e instruções para o jogador:
    - ESCAPE / Q : sair do jogo
    - SPACE      : reiniciar
    - R          : abrir ranking
    """

    def __init__(self, window, assets):
        """Inicializa a tela de Game Over.

        Args:
            window (pygame.Surface): Superfície principal onde a tela é desenhada.
            assets (dict): Dicionário de recursos (imagens, fontes, sons, etc.).
        """
        self.window = window
        self.assets = assets

    def handle_event(self, event):
        """Processa eventos de teclado relevantes para a tela de Game Over.

        Mapeia teclas para ações que serão interpretadas pelo loop principal.

        Args:
            event (pygame.event.Event): Evento Pygame a ser processado.

        Returns:
            str | None: Uma string representando a ação solicitada:
                - 'SAIR' para encerrar o jogo,
                - 'RESTART' para reiniciar,
                - 'RANKING' para ir ao ranking,
                - None se nenhum comando relevante for detectado.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                return 'SAIR'
            if event.key == pygame.K_SPACE:
                return 'RESTART'
            if event.key == pygame.K_r:
                return 'RANKING'
        return None

    def update(self, dt):
        """Atualiza o estado da tela.

        Esta tela é estática, portanto apenas retorna seu identificador.

        Args:
            dt (float): Delta time em segundos (não utilizado aqui).

        Returns:
            str: 'GAMEOVER' (identificador da tela).
        """
        return 'GAMEOVER'

    def draw(self):
        """Desenha a tela de Game Over na janela.

        Exibe o fundo, a imagem de game over e instruções centrais.
        """
        self.window.fill((0, 100, 100))
        self.window.blit(self.assets['game_over'], (0, 0))

        txt = self.assets['fonte2'].render("PRESSIONE SPACE PARA RECOMEÇAR", True, (255, 255, 255))
        pos_x_txt = self.window.get_width() // 2 - txt.get_width() // 2

        rank = self.assets['fonte2'].render("PRESSIONE R PARA VER RANKING", True, (255, 255, 255))
        pos_x_rank = self.window.get_width() // 2 - rank.get_width() // 2

        # posições fixas próximas à base da tela (preservando seu layout original)
        self.window.blit(txt, (pos_x_txt, 750))
        self.window.blit(rank, (pos_x_rank, 800))
