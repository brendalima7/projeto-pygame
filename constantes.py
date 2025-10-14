import pygame

pygame.init()
info = pygame.display.Info()

WINDOWWIDHT = info.current_w
WINDOWHEIGHT = info.current_h

# dimensoes do mapa
map_surface = pygame.image.load('assets/ground.png')
MAP_W, MAP_H = map_surface.get_size()

# cores e outros valores
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
VERDE_MAPA = (34, 139, 34)
TILE_SIZE = 64