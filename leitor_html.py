# leitor_html.py
from bs4 import BeautifulSoup
import re
import os

def carregar_soup(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        print(f"❌ Arquivo {caminho_arquivo} não encontrado!")
        return None
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            # lxml é essencial para arquivos de 11MB
            return BeautifulSoup(f, 'lxml')
    except Exception as e:
        print(f"❌ Erro ao abrir HTML: {e}")
        return None

def buscar_produto_na_base(soup, codigo_procurado):
    try:
        # Padroniza: '004430' -> '4430'
        cod_alvo = str(int(re.sub(r'\D', '', str(codigo_procurado))))
        
        linhas = soup.find_all('tr')
        for linha in linhas:
            colunas = linha.find_all('td')
            if len(colunas) > 3:
                texto_coluna = colunas[2].get_text(strip=True)
                cod_bruto = re.sub(r'\D', '', texto_coluna)
                
                if cod_bruto:
                    cod_local = str(int(cod_bruto))
                    if cod_local == cod_alvo:
                        return colunas[3].get_text(strip=True).upper()
    except:
        pass
    return None