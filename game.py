import pygame

# variaveis globais
WINDOWWIDHT = 800
WINDOWHEIGHT = 600

window = pygame.display.set_mode((WINDOWWIDHT, WINDOWHEIGHT))
pygame.display.set_caption('SWITCH BACK')

def condicoes_iniciais(): 
    assets = {}
    # jogador
    assets['jogador'] = pygame.transform.scale(pygame.image.load('assets/ball.png'), (50,50))
    return assets

class Jogador (pygame.sprite.Sprite):
    def __init__(self,assets):
        pygame.sprite.Sprite.__init__(self)
        self.assets = assets
        self.image = assets['jogador']
        self.x = 500
        self.y = 200

    def draw(self):
        window.blit(self.image, (self.x, self.y))

# elementos jogáveis e lógica de interação
class TelaJogo:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets  
        self.jogador = Jogador(assets)  
    def draw(self):
        self.window.fill((0, 0, 0))
        self.jogador.draw() 
    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
                    return False       
        return True

class Jogo:
    def __init__(self):
        pygame.init()
        self.window = window
        self.assets = condicoes_iniciais()
        self.telajogo = TelaJogo(window,self.assets)
        self.jogador = Jogador(self.assets)

    # loop principal
    def run(self):
        rodando = True 
        while rodando:
            mantem_rodando = self.telajogo.update()      
            if not mantem_rodando:
                rodando = False 
            self.telajogo.draw()
            pygame.display.update()           
        pygame.quit() 
            
if __name__ == '__main__':
    game = Jogo()
    game.run()

