import pygame
from constantes import *  # PRETO, VERMELHO, AZUL, WINDOWWIDHT, WINDOWHEIGHT

class TelaVitoria:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets
        self.tempo_final_ms = 0
        self.nome_jogador = ""
        
    def set_tempo_final(self, tempo_ms, nome):
        """Define apenas os dados a mostrar (não salva mais aqui)."""
        self.tempo_final_ms = tempo_ms
        self.nome_jogador = nome

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Retorna para o ranking quando o jogador pressiona R
                payload = {'nome': self.nome_jogador, 'tempo_ms': self.tempo_final_ms}
                return 'RANKING', payload
        return None

    def update(self, dt):
        return 'VITORIA'  # Mantém o estado

    def draw(self):
        self.window.fill(PRETO) 
        self.window.blit(self.assets['tela_vitoria'], (0, 0))
        
        # tempo fromatado
        total_segundos = self.tempo_final_ms // 1000
        ms = self.tempo_final_ms % 1000
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        tempo_formatado = f"{minutos:02}:{segundos:02}:{ms//10:02}"  # 2 dígitos de ms

        texto_tempo = f"TEMPO: {tempo_formatado}"
        img_tempo = self.assets['fonte2'].render(texto_tempo, True, (0, 255, 0))
        rect_tempo = img_tempo.get_rect(center=(WINDOWWIDHT // 2, WINDOWHEIGHT - 100))
        self.window.blit(img_tempo, rect_tempo)

        # instrucao
        texto_instrucao = "PRESSIONE R PARA ACESSAR O RANKING"
        img_instrucao = self.assets['fonte2'].render(texto_instrucao, True, (255, 255, 255))
        rect_instrucao = img_instrucao.get_rect(center=(WINDOWWIDHT // 2, WINDOWHEIGHT - 50))
        self.window.blit(img_instrucao, rect_instrucao)

