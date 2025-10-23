"""
Tela de instruções (parte 2) do jogo SWITCH BACK.

Exibe a segunda tela de instruções, geralmente com informações finais
ou dicas antes de iniciar o jogo propriamente dito.
"""

import pygame


class TelaInstrucoes2:
    """Tela de instruções 2 do jogo SWITCH BACK.

    Mostra a segunda parte das instruções e permite ao jogador
    iniciar o jogo ou sair.
    """

    def __init__(self, window, assets):
        """Inicializa a tela de instruções 2.

        Args:
            window (pygame.Surface): Superfície principal de exibição.
            assets (dict): Dicionário de recursos (imagens, fontes, etc.).
        """
        self.window = window
        self.assets = assets    

    def handle_event(self, event):
        """Processa eventos de teclado para navegação.

        - ESC / Q: encerra o jogo.
        - ENTER: inicia o jogo.

        Args:
            event (pygame.event.Event): Evento Pygame capturado no loop principal.

        Returns:
            str | None:  
                'SAIR' para encerrar,  
                'JOGO' para iniciar,  
                None se nenhuma ação relevante for detectada.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                return 'SAIR'
            if event.key == pygame.K_RETURN:
                return 'JOGO'
        return None

    def update(self, dt):
        """Atualiza o estado da tela.

        Esta tela é estática, portanto apenas retorna seu identificador.

        Args:
            dt (float): Delta time (não utilizado aqui).

        Returns:
            str: 'INSTRUCOES2' (identificador da tela).
        """
        return 'INSTRUCOES2'

    def draw(self):
        """Desenha a tela de instruções 2 na janela."""
        self.window.fill((0, 100, 100))
        self.window.blit(self.assets['tela_instrucoes2'], (0, 0))
