"""
Constantes do jogo SWITCH BACK.

Este módulo centraliza configurações globais usadas em várias telas e
módulos do jogo, incluindo dimensões da janela, tamanho das tiles,
cores, fatores de parallax e parâmetros físicos simples (gravidade,
velocidade vertical, tempo de mudança de gravidade).

As unidades e convenções principais:
- Todas as dimensões estão em pixels.
- Tempos estão em milissegundos quando aplicável (ex.: `tempo_mudanca_gravidade`).
- As cores são tuplas RGB ou strings hex, conforme usadas nas renderizações.
"""

import pygame
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame
pygame.init()

# largura e altura da janela (obtidas dinamicamente)
info = pygame.display.Info()
WINDOWWIDHT = info.current_w
WINDOWHEIGHT = info.current_h

# Base do tile e fator de escala:
BASE_TILE_SIZE = 16      # tamanho base da tile (px)
SCALE_FACTOR = 4         # fator de escala aplicado ao tamanho base
TILE_SIZE = BASE_TILE_SIZE * SCALE_FACTOR  # tamanho final da tile (px)

# cores e outros valores
PRETO = (0, 0, 0)
AZUL = '#207bfa'
VERMELHO = (255, 0, 0)
VERDE_MAPA = (34, 139, 34)
COR_FUNDO = '#FFFFFF'
PARALLAX_FACTOR = 0.3

# parâmetros de física / movimento (valores em px / s² ou px/s conforme uso)
gravidade_normal = 50         # gravidade padrão (positiva p/ puxar para baixo)
gravidade_invertida = -50     # gravidade invertida (puxa para cima)
velocidade_y = -20            # velocidade vertical inicial (quando aplicável)
velocidade_y_invertido = 20   # velocidade vertical inicial com gravidade invertida

# tempo para alternar gravidade (milissegundos)
tempo_mudanca_gravidade = 12000
