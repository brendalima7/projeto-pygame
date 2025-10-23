import pygame
import json
import os
from constantes import *
from tela_vitoria import RANKING_FILE 

class TelaRanking:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets
        self.ranking_data = self._carregar_ranking()
        self.font = self.assets['fonte']
        self.pequena_font = self.assets['fonte2']
        
    def _carregar_ranking(self):
        if not os.path.exists(RANKING_FILE):
            return []
        
        with open(RANKING_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
                
    def _formatar_tempo(self, tempo_ms):
        total_segundos = tempo_ms // 1000
        ms = tempo_ms % 1000
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        return f"{minutos:02}:{segundos:02}.{ms:03}"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return 'INICIO'
        return None

    def update(self, dt):
        self.ranking_data = self._carregar_ranking()
        return 'RANKING'

    def draw(self):
        self.window.fill(PRETO) 
        
        # titulo
        texto_titulo = "RANKING SPEEDRUN"
        img_titulo = self.font.render(texto_titulo, True, (255, 255, 255))
        rect_titulo = img_titulo.get_rect(center=(WINDOWWIDHT // 2, 50))
        self.window.blit(img_titulo, rect_titulo)
        
        # cabecalho da tela
        header_text = "POS.   NOME            TEMPO"
        img_header = self.pequena_font.render(header_text, True, AZUL) # Usando AZUL
        self.window.blit(img_header, (WINDOWWIDHT // 2 - img_header.get_width() // 2, 120))
        
        # desenha os resultados
        y_start = 180
        if not self.ranking_data:
            texto_vazio = "Nenhum recorde encontrado!"
            img_vazio = self.pequena_font.render(texto_vazio, True, (255, 255, 255))
            self.window.blit(img_vazio, (WINDOWWIDHT // 2 - img_vazio.get_width() // 2, y_start))
        else:
            for i, record in enumerate(self.ranking_data):
                posicao = f"{i + 1:02d}"
                nome = record.get('nome', 'N/A')[:15].ljust(15)
                tempo_ms = record.get('tempo_ms', 999999000)
                tempo_formatado = self._formatar_tempo(tempo_ms)

                linha_ranking = f"{posicao}.   {nome}   {tempo_formatado}"
                
                # cores diferentes para o TOP 3
                if i == 0:
                    cor = (255, 215, 0) # ouro
                elif i == 1:
                    cor = (192, 192, 192) # prata
                elif i == 2:
                    cor = (205, 127, 50) # bronze
                else:
                    cor = (255, 255, 255) # branco
                    
                img_linha = self.pequena_font.render(linha_ranking, True, cor)
                
                x_pos = WINDOWWIDHT // 2 - img_linha.get_width() // 2 
                self.window.blit(img_linha, (x_pos, y_start + i * 40))
                
        # dica para retornar
        texto_retorno = "PRESSIONE ENTER PARA RETORNAR"
        img_retorno = self.pequena_font.render(texto_retorno, True, (150, 150, 150))
        rect_retorno = img_retorno.get_rect(center=(WINDOWWIDHT // 2, WINDOWHEIGHT - 50))
        self.window.blit(img_retorno, rect_retorno)