"""
Tela de entrada de nome do jogador para o jogo SWITCH BACK.

Contém:
- A classe `InputBox`, que gerencia o campo de texto com cursor piscante e validação.
- A classe `TelaInputNome`, que exibe o fundo e integra a caixa de entrada ao fluxo do jogo.
"""

import pygame
from constantes import * 

# Cores usadas no campo de texto
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_TEXT = pygame.Color('white')


class InputBox:
    """Campo de texto interativo para entrada de nome do jogador.

    Permite digitação limitada (máx. 10 caracteres), exibe cursor piscante
    e retorna o texto completo quando o jogador pressiona ENTER.
    """

    def __init__(self, x, y, w, h, font, text=''):
        """Inicializa o campo de entrada de texto.

        Args:
            x (int): Posição X do canto superior esquerdo.
            y (int): Posição Y do canto superior esquerdo.
            w (int): Largura da caixa.
            h (int): Altura da caixa.
            font (pygame.font.Font): Fonte usada para renderizar o texto.
            text (str, optional): Texto inicial (padrão: '').
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_ACTIVE
        self.text = text
        self.font = font
        self.active = True
        self.txt_surface = font.render(text, True, COLOR_TEXT)
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = 10  # Limite de caracteres permitidos

    def handle_event(self, event):
        """Processa eventos de teclado e atualiza o texto.

        - ENTER confirma o nome (se não vazio);
        - BACKSPACE apaga um caractere;
        - Letras e números são adicionados (em maiúsculo);
        - Cursor piscante é reiniciado a cada digitação.

        Args:
            event (pygame.event.Event): Evento Pygame de teclado.

        Returns:
            tuple[str | None, str | None]:  
                ('COMPLETO', texto) se ENTER for pressionado com texto válido,  
                (None, None) caso contrário.
        """
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.text.strip(): 
                        return 'COMPLETO', self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.max_length:
                    if event.unicode.isalnum() or event.unicode.isspace():
                        self.text += event.unicode.upper() 
                
                self.txt_surface = self.font.render(self.text, True, COLOR_TEXT)
                self.cursor_timer = 0 
        
        return None, None 

    def update(self, dt):
        """Atualiza o estado do cursor piscante.

        Args:
            dt (float): Delta time (não utilizado, contador é baseado em frames).
        """
        self.cursor_timer += 1
        if self.cursor_timer > 30: 
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, screen):
        """Desenha a caixa de texto, o texto e o cursor piscante.

        Args:
            screen (pygame.Surface): Superfície onde desenhar a caixa.
        """
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 3) 
        
        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + self.txt_surface.get_width()
            cursor_y = self.rect.y + 5
            cursor_h = self.rect.h - 10 
            pygame.draw.line(screen, COLOR_TEXT, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_h), 2)


class TelaInputNome:
    """Tela responsável pela entrada de nome do jogador.

    Exibe o fundo personalizado e uma `InputBox` para digitação do nome.
    Controla a transição para outras telas (instruções, sair, etc.).
    """

    def __init__(self, window, assets):
        """Inicializa a tela e cria a caixa de entrada centralizada.

        Args:
            window (pygame.Surface): Superfície principal do jogo.
            assets (dict): Dicionário de recursos (imagens, fontes, etc.).
        """
        self.window = window
        self.assets = assets

        largura = 350
        altura = 60
        x = (WINDOWWIDHT // 2) - (largura // 2)
        y = (WINDOWHEIGHT // 2)
        
        self.input_box = InputBox(x, y, largura, altura, self.assets['fonte2'])

    def handle_event(self, event):
        """Processa eventos de teclado e interações com a caixa de texto.

        - ESC: encerra o jogo;
        - ENTER: vai para tela de instruções;
        - ENTER dentro da caixa (com texto válido): retorna nome e estado 'INICIO'.

        Args:
            event (pygame.event.Event): Evento Pygame de teclado.

        Returns:
            tuple[str, str] | str | None:  
                ('INICIO', nome) quando o nome for confirmado,  
                'SAIR' ou 'INSTRUCOES1' conforme tecla pressionada,  
                None se nenhuma ação relevante ocorrer.
        """
        retorno, nome_digitado = self.input_box.handle_event(event)
        
        if retorno == 'COMPLETO':
            # Retorna o próximo estado ('INICIO') E o nome capturado
            return 'INICIO', nome_digitado.strip()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return 'SAIR'
            if event.key == pygame.K_RETURN:
                return 'INSTRUCOES1'
            
        return None

    def update(self, dt):
        """Atualiza o estado da tela (animações, cursor, etc.).

        Args:
            dt (float): Delta time em segundos.

        Returns:
            str: 'INPUT_NOME' (identificador desta tela).
        """
        self.input_box.update(dt)
        return 'INPUT_NOME'

    def draw(self):
        """Desenha o fundo, o texto de instrução e a caixa de entrada."""
        self.window.fill((0, 0, 0))
        self.window.blit(self.assets['tela_nome'], (0, 0))

        # Renderiza o texto de instrução
        instrucao = self.assets['fonte2'].render("DIGITE SEU NOME (ENTER):", True, (200, 200, 200))

        # Margem inferior da tela
        margem_inferior = 80

        # Posição Y para a caixa de input e o texto
        input_y = WINDOWHEIGHT - margem_inferior - self.input_box.rect.height
        text_y = input_y - 60  # o texto fica acima da caixa

        # Atualiza a posição da caixa de input
        self.input_box.rect.center = (WINDOWWIDHT // 2, input_y)

        # Centraliza o texto horizontalmente
        rect_instrucao = instrucao.get_rect(center=(WINDOWWIDHT // 2, text_y))

        # Desenha texto e input
        self.window.blit(instrucao, rect_instrucao)
        self.input_box.draw(self.window)
