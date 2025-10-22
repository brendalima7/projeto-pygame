import json
import os

ARQUIVO_RANKING = 'ranking.json'
MAX_REGISTROS = 10  # Limite o ranking ao Top 10

# DADOS PADRÃO/BACKUP: Usados se o arquivo fixo for perdido/corrompido.
# Tempo em milissegundos (menor é melhor)
RANKING_PADRAO = [
    {"nome": "DEV", "tempo_ms": 150000},  # 2m 30s
    {"nome": "GHOST", "tempo_ms": 240000} # 4m 00s
]

def carregar_ranking():
    """
    Lê o ranking do arquivo JSON. 
    Se o arquivo falhar ou não existir, retorna o RANKING_PADRAO.
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
    """
    Salva a lista de dados do ranking no arquivo JSON.
    """
    try:
        with open(ARQUIVO_RANKING, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4)
    except Exception as e:
        print(f"[ERRO RANKING] Erro ao salvar: {e}")

def adicionar_tempo(nome, tempo_ms): # <--- MUDANÇA DE NOME E PARÂMETRO
    """
    Adiciona um novo registro ao ranking, ordena e limita a lista.
    O critério de ordenação é o tempo (menor tempo primeiro).
    """
    ranking = carregar_ranking()
    
    # Adiciona o novo registro
    novo_registro = {"nome": nome.strip().upper(), "tempo_ms": tempo_ms} # <--- NOVO CAMPO
    ranking.append(novo_registro)
    
    # ORDENAÇÃO CHAVE: Ordena pelo 'tempo_ms', do menor para o maior (reverse=False)
    ranking.sort(key=lambda item: item['tempo_ms'], reverse=False) 
    
    # Limita (ao Top N)
    ranking = ranking[:MAX_REGISTROS]
    
    salvar_ranking(ranking)
    
    return ranking