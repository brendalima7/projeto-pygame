import pygame
from os import walk
from os.path import join
from pytmx.util_pygame import load_pygame
pygame.init()

# largura e altura da janela 
info = pygame.display.Info()
WINDOWWIDHT = info.current_w
WINDOWHEIGHT = info.current_h

BASE_TILE_SIZE = 16  
SCALE_FACTOR = 4     
TILE_SIZE = BASE_TILE_SIZE * SCALE_FACTOR

# dimensoes do mapa
map_surface = pygame.image.load('assets/ground.png')
MAP_W, MAP_H = map_surface.get_size()

# cores e outros valores
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE_MAPA = (34, 139, 34)
COR_FUNDO = '#FFFFFF'