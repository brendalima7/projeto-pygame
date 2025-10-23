import pygame
import json
import os
from constantes import *

RANKING_FILE = 'ranking.json'  # agora o arquivo de ranking vive aqui

class TelaRanking:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets
        self.ranking_data = self._carregar_ranking()
        self.font = self.assets['fonte']
        self.pequena_font = self.assets['fonte2']

        # Opções de ação
        self.opcoes = ['REINICIAR', 'MENU PRINCIPAL', 'SAIR']
        self.indice_selecionado = 0

        # ---- Novo: carrega imagem de fundo ----
        caminho_fundo = os.path.join('assets', 'new.png')
        if os.path.exists(caminho_fundo):
            self.fundo = pygame.transform.scale(
                pygame.image.load(caminho_fundo).convert(),
                (WINDOWWIDHT, WINDOWHEIGHT)
            )
        else:
            self.fundo = None

    # ranking file handling 
    def _carregar_ranking(self):
        if not os.path.exists(RANKING_FILE):
            return []
        with open(RANKING_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _salvar_ranking(self, ranking):
        with open(RANKING_FILE, 'w') as f:
            json.dump(ranking, f, indent=4)

    def add_result(self, nome, tempo_ms):
        """Adicionar um novo resultado ao ranking, ordenar e salvar (máx 10)."""
        if nome is None:
            nome = "Player"
        novo_resultado = {'nome': nome, 'tempo_ms': tempo_ms}

        ranking = self._carregar_ranking()
        ranking.append(novo_resultado)
        ranking.sort(key=lambda x: x['tempo_ms'])
        ranking = ranking[:10]
        self._salvar_ranking(ranking)

        self.ranking_data = ranking

    # formatação 
    def _formatar_tempo(self, tempo_ms):
        total_segundos = tempo_ms // 1000
        ms = tempo_ms % 1000
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        return f"{minutos:02}:{segundos:02}.{ms:03}"

    # input / navegação
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)
            elif event.key == pygame.K_DOWN:
                self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)
            elif event.key == pygame.K_RETURN:
                selecionada = self.opcoes[self.indice_selecionado]
                if selecionada == 'REINICIAR':
                    return 'RESTART'
                elif selecionada == 'MENU PRINCIPAL':
                    return 'INICIO'
                elif selecionada == 'SAIR':
                    return 'SAIR'
        return None

    def update(self, dt):
        self.ranking_data = self._carregar_ranking()
        return 'RANKING'

    def draw(self):
        
        if self.fundo:
            self.window.blit(self.fundo, (0, 0))
        else:
            self.window.fill(PRETO)

       
        texto_titulo = "RANKING SPEEDRUN"
        img_titulo = self.font.render(texto_titulo, True, (255, 255, 255))
        rect_titulo = img_titulo.get_rect(center=(WINDOWWIDHT // 2, 50))
        self.window.blit(img_titulo, rect_titulo)

        
        header_text = "POS.   NOME            TEMPO"
        img_header = self.pequena_font.render(header_text, True, AZUL)
        self.window.blit(img_header, (WINDOWWIDHT // 2 - img_header.get_width() // 2, 120))

        
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

                if i == 0:
                    cor = (255, 215, 0)
                elif i == 1:
                    cor = (192, 192, 192)
                elif i == 2:
                    cor = (205, 127, 50)
                else:
                    cor = (255, 255, 255)

                img_linha = self.pequena_font.render(linha_ranking, True, cor)
                x_pos = WINDOWWIDHT // 2 - img_linha.get_width() // 2
                self.window.blit(img_linha, (x_pos, y_start + i * 40))

     
        y_opcoes = WINDOWHEIGHT - 140
        for i, opcao in enumerate(self.opcoes):
            cor = VERMELHO if i == self.indice_selecionado else (200, 200, 200)
            img_opcao = self.pequena_font.render(opcao, True, cor)
            rect_opcao = img_opcao.get_rect(center=(WINDOWWIDHT // 2, y_opcoes + i * 40 - 20))
            self.window.blit(img_opcao, rect_opcao)
