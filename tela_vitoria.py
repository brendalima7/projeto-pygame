import pygame
import json
import os
from constantes import * # Importa PRETO, VERMELHO, AZUL, WINDOWWIDHT, WINDOWHEIGHT

# Nome do arquivo de ranking (Pode ser definido aqui ou no ranking_manager)
RANKING_FILE = 'ranking.json'

class TelaVitoria:
    def __init__(self, window, assets):
        self.window = window
        self.assets = assets # Agora usamos este para as fontes
        self.tempo_final_ms = 0
        self.nome_jogador = "Player"
        
        # Ações do menu (RESTART/SAIR)
        self.opcoes = ['REINICIAR', 'MENU PRINCIPAL', 'SAIR']
        self.indice_selecionado = 0
        self.ranking_salvo = False # fflag para garantir que salva apenas uma vez
        
    def set_tempo_final(self, tempo_ms, nome):
        """Define o tempo final e salva o ranking."""
        self.tempo_final_ms = tempo_ms
        self.nome_jogador = nome
        
        if not self.ranking_salvo:
            self._salvar_ranking()
            self.ranking_salvo = True

    def _salvar_ranking(self):
        """Carrega, adiciona o novo resultado, ordena e salva o ranking."""
        novo_resultado = {
            'nome': self.nome_jogador,
            'tempo_ms': self.tempo_final_ms
        }
        
        ranking = []
        if os.path.exists(RANKING_FILE):
            try:
                with open(RANKING_FILE, 'r') as f:
                    ranking = json.load(f)
            except json.JSONDecodeError:
                ranking = []

        ranking.append(novo_resultado)
        ranking.sort(key=lambda x: x['tempo_ms'])
        ranking = ranking[:10] 
        
        with open(RANKING_FILE, 'w') as f:
            json.dump(ranking, f, indent=4)
            
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.indice_selecionado = (self.indice_selecionado - 1) % len(self.opcoes)
            elif event.key == pygame.K_DOWN:
                self.indice_selecionado = (self.indice_selecionado + 1) % len(self.opcoes)
            elif event.key == pygame.K_RETURN:
                if self.opcoes[self.indice_selecionado] == 'REINICIAR':
                    return 'RESTART', None
                elif self.opcoes[self.indice_selecionado] == 'MENU PRINCIPAL':
                    return 'INICIO', None 
                elif self.opcoes[self.indice_selecionado] == 'SAIR':
                    return 'SAIR', None
        return None

    def update(self, dt):
        return 'VITORIA' # Mantém o estado

    def draw(self):
        # Usando PRETO do seu arquivo constantes.py como cor de fundo
        self.window.fill(PRETO) 
        
        # Converte o tempo
        total_segundos = self.tempo_final_ms // 1000
        ms = self.tempo_final_ms % 1000
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        tempo_formatado = f"{minutos:02}:{segundos:02}.{ms:03}"
        
        # Título de Vitória (Branco)
        texto_vitoria = "VITÓRIA!"
        img_vitoria = self.assets['fonte'].render(texto_vitoria, True, (255, 255, 255))
        rect_vitoria = img_vitoria.get_rect(center=(WINDOWWIDHT // 2, WINDOWHEIGHT // 4))
        self.window.blit(img_vitoria, rect_vitoria)

        # Tempo Final (VERDE)
        texto_tempo = f"Tempo Final: {tempo_formatado}"
        img_tempo = self.assets['fonte2'].render(texto_tempo, True, VERDE_MAPA) # Usando VERDE_MAPA como uma cor agradável
        rect_tempo = img_tempo.get_rect(center=(WINDOWWIDHT // 2, WINDOWHEIGHT // 4 + 70))
        self.window.blit(img_tempo, rect_tempo)
        
        # Nome do Jogador (Branco)
        texto_nome = f"JOGADOR: {self.nome_jogador}"
        img_nome = self.assets['fonte2'].render(texto_nome, True, (255, 255, 255))
        rect_nome = img_nome.get_rect(center=(WINDOWWIDHT // 2, WINDOWHEIGHT // 4 + 110))
        self.window.blit(img_nome, rect_nome)

        # Desenha as opções do menu
        y_start = WINDOWHEIGHT // 2
        for i, opcao in enumerate(self.opcoes):
            # Selecionado: VERMELHO, Não Selecionado: AZUL
            cor = VERMELHO if i == self.indice_selecionado else AZUL 
            img_opcao = self.assets['fonte2'].render(opcao, True, cor)
            rect_opcao = img_opcao.get_rect(center=(WINDOWWIDHT // 2, y_start + i * 50))
            self.window.blit(img_opcao, rect_opcao)