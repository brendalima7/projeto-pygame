import pygame

class Jogador (pygame.sprite.Sprite):
    def __init__(self, window, assets):
        pygame.sprite.Sprite.__init__(self)
        self.window = window
        self.assets = assets
        self.image = assets['jogador']
        self.x = 500
        self.y = 200

    def draw(self):
        self.window.blit(self.image, (self.x, self.y))