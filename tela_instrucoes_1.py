"""
Tela de instruções (parte 1) do jogo SWITCH BACK.

Exibe a primeira tela de instruções para o jogador, com teclas de controle
e informações iniciais sobre o funcionamento do jogo.
"""

import pygame


class TelaInstrucoes1:
    """Tela de instruções inicial do jogo.

    Mostra informações básicas sobre controles e regras do jogo.
    Permite ao jogador avançar para a segunda tela de instruções ou sair.
    """

    def __init__(self, window, assets):
        """Inicializa a tela de instruções 1.

        Args:
            window (pygame.Surface): Superfície principal do jogo.
            assets (dict): Dicionário de recursos (imagens, fontes, etc.).
        """
        self.window = window
        self.assets = assets    

    def handle_event(self, event):
        """Processa eventos de teclado para navegação entre telas.

        - ESC / Q: encerra o jogo.
        - ENTER: avança para a próxima tela de instruções.

        Args:
            event (pygame.event.Event): Evento Pygame capturado no loop principal.

        Returns:
            str | None:  
                'SAIR' para encerrar,  
                'INSTRUCOES2' para avançar,  
                None se nenhuma ação for detectada.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                return 'SAIR'
            if event.key == pygame.K_RETURN:
                return 'INSTRUCOES2'
        return None

    def update(self, dt):
        """Atualiza o estado da tela.

        Esta tela é estática, portanto apenas retorna seu identificador.

        Args:
            dt (float): Delta time (não utilizado nesta tela).

        Returns:
            str: 'INSTRUCOES1' (identificador da tela).
        """
        return 'INSTRUCOES1'

    def draw(self):
        """Desenha a tela de instruções 1 na janela."""
        self.window.fill((0, 100, 100))
        self.window.blit(self.assets['tela_instrucoes1'], (0, 0))
