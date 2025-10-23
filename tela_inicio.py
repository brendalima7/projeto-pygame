"""
Tela inicial do jogo SWITCH BACK.

Exibe o fundo e a mensagem "PRESSIONE SPACE PARA JOGAR" com efeito de
fade in/out. Também trata eventos de teclado para iniciar o jogo ou sair.
"""

import pygame 


class TelaInicio:
    """Tela inicial (menu principal) do jogo.

    Mostra a imagem de fundo e um texto piscante instruindo o jogador a iniciar.
    """

    def __init__(self, window, assets):
        """Inicializa a tela de início.

        Args:
            window (pygame.Surface): Superfície principal de exibição do jogo.
            assets (dict): Dicionário de recursos (imagens, fontes, etc.).
        """
        self.window = window
        self.assets = assets

        self.alpha = 0                 # Valor atual de transparência do texto
        self.fade_speed = 600          # Velocidade do fade (quanto maior, mais rápido)
        self.fade_direction = 1        # 1 para aumentar alpha, -1 para diminuir
        
    def handle_event(self, event):
        """Processa eventos de teclado para esta tela.

        Mapeia teclas de ação para os estados do jogo:
        - ESCAPE ou Q: sair do jogo
        - SPACE: ir para tela de entrada de nome

        Args:
            event (pygame.event.Event): Evento Pygame capturado no loop principal.

        Returns:
            str | None: O próximo estado do jogo ou None se nenhuma ação for tomada.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return 'SAIR'
            if event.key == pygame.K_SPACE:
                return 'INPUT_NOME'
        return None
        
    def update(self, dt):
        """Atualiza o estado da tela, aplicando o efeito de fade no texto.

        O valor de alpha oscila entre 0 e 255 continuamente, criando um
        efeito de piscar ("Pressione SPACE para jogar").

        Args:
            dt (float): Delta time em segundos.

        Returns:
            str: 'INICIO' (identificador desta tela).
        """
        self.alpha += self.fade_direction * self.fade_speed * dt 
        if self.alpha >= 255:
            self.alpha = 255
            self.fade_direction = -1  # Começa a diminuir
        elif self.alpha <= 0:
            self.alpha = 0
            self.fade_direction = 1 
        return 'INICIO'
    
    def draw(self):
        """Desenha o fundo e o texto piscante na tela."""
        self.window.fill((0, 100, 100))
        self.window.blit(self.assets['fundo_inicial'], (0, 0))

        # Texto com efeito de fade
        img_tempo = self.assets['fonte2'].render("PRESSIONE SPACE PARA JOGAR", True, (255, 255, 255))
        img_tempo.set_alpha(int(self.alpha))
        pos_x = self.window.get_width() // 2 - img_tempo.get_width() // 2
        self.window.blit(img_tempo, (pos_x, 720))
