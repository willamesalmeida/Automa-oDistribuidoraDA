# validador.py
from rapidfuzz import fuzz

def validar_produto(nome_site, nome_local, margem=50):
    # Limpa nomes para comparação (caixa alta e sem espaços extras)
    s = nome_site.upper().strip()
    l = nome_local.upper().strip()
    
    score = fuzz.token_sort_ratio(s, l)
    return score >= margem, score