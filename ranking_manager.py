"""
Módulo de gerenciamento do ranking do jogo SWITCH BACK.

Este módulo define funções utilitárias para:
    - Carregar e salvar o ranking de tempos (em milissegundos);
    - Adicionar novos resultados e manter apenas os 10 melhores tempos;
    - Garantir recuperação segura em caso de arquivo corrompido ou ausente.
"""

import json
import os

# Caminho padrão do arquivo de ranking
ARQUIVO_RANKING = 'ranking.json'

# Número máximo de registros mantidos
MAX_REGISTROS = 10  # Limite o ranking ao Top 10

# DADOS PADRÃO/BACKUP: Usados se o arquivo fixo for perdido/corrompido.
# Tempo em milissegundos (menor é melhor)
RANKING_PADRAO = [
    {"nome": "DEV", "tempo_ms": 150000},  # 2m 30s
    {"nome": "GHOST", "tempo_ms": 240000} # 4m 00s
]


def carregar_ranking():
    """Carrega o ranking do arquivo JSON.

    Lê o conteúdo de ``ARQUIVO_RANKING`` e retorna uma lista de dicionários,
    cada um contendo ``nome`` e ``tempo_ms``.  
    Caso o arquivo não exista, esteja vazio ou corrompido, retorna
    o ``RANKING_PADRAO``.

    Returns:
        list[dict]: Lista de registros do ranking, onde cada item contém:
            - ``nome`` (str): Nome do jogador.
            - ``tempo_ms`` (int): Tempo em milissegundos.
    """
    if not os.path.exists(ARQUIVO_RANKING):
        return RANKING_PADRAO
    
    try:
        with open(ARQUIVO_RANKING, 'r', encoding='utf-8') as f:
            conteudo = f.read()
            if not conteudo:
                return RANKING_PADRAO
            return json.loads(conteudo)
    except json.JSONDecodeError:
        print(f"[ERRO RANKING] Conteúdo de {ARQUIVO_RANKING} inválido. Usando ranking padrão.")
        return RANKING_PADRAO
    except Exception as e:
        print(f"[ERRO RANKING] Erro ao carregar: {e}. Usando ranking padrão.")
        return RANKING_PADRAO


def salvar_ranking(dados):
    """Salva a lista de dados do ranking no arquivo JSON.

    Args:
        dados (list[dict]): Lista de registros com chaves ``nome`` e ``tempo_ms``.
    """
    try:
        with open(ARQUIVO_RANKING, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4)
    except Exception as e:
        print(f"[ERRO RANKING] Erro ao salvar: {e}")


def adicionar_tempo(nome, tempo_ms):
    """Adiciona um novo tempo ao ranking e mantém apenas os melhores resultados.

    O novo registro é adicionado à lista atual, que é então ordenada em ordem
    crescente de ``tempo_ms`` (menores tempos primeiro).  
    Apenas os ``MAX_REGISTROS`` melhores tempos são mantidos.

    Args:
        nome (str): Nome do jogador a ser adicionado no ranking.
        tempo_ms (int): Tempo total do jogador em milissegundos.

    Returns:
        list[dict]: Lista atualizada dos melhores tempos (Top 10).
    """
    ranking = carregar_ranking()
    
    # Adiciona o novo registro
    novo_registro = {"nome": nome.strip().upper(), "tempo_ms": tempo_ms}
    ranking.append(novo_registro)
    
    # Ordena pelo menor tempo
    ranking.sort(key=lambda item: item['tempo_ms'], reverse=False) 
    
    # Limita ao Top N
    ranking = ranking[:MAX_REGISTROS]
    
    salvar_ranking(ranking)
    
    return ranking
