# 🤖 Automação de Ativos Digitais — DA Distribuidora Arapiraca

Sistema interno de extração, validação e sincronização de imagens de produtos, desenvolvido para uso exclusivo da **DA Distribuidora Arapiraca**.

## 📋 Sobre o Projeto

O sistema foi criado para automatizar a ponte entre o e-commerce (**WooCommerce**) e o ERP (**TOTVS WinThor**), permitindo:
* **Scraping de Alta Performance:** Navegação automatizada no site para coleta de imagens originais.
* **Validação Fuzzy:** Comparação inteligente de nomes de produtos (Site vs. WinThor) para garantir que a foto pertence ao item correto.
* **Mapeamento Multi-Código:** Tratamento de produtos que possuem múltiplos SKUs/códigos (ex: tanques e conexões).
* **Gestão de Acervo:** Download organizado de fotos renomeadas automaticamente pelo código interno do ERP.

## 🖥️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
| :--- | :--- |
| **Python 3.12+** | Linguagem principal do sistema |
| **Selenium** | Automação de navegador para navegação dinâmica |
| **BeautifulSoup4** | Parsing e leitura de base de dados HTML (WinThor) |
| **RapidFuzz** | Algoritmo de similaridade de strings (Levenshtein) |
| **Requests** | Gerenciamento de downloads e requisições HTTP |
| **Regex (re)** | Extração e sanitização de múltiplos códigos |
| **Webdriver-Manager** | Gestão automatizada de drivers do navegador |

## 📁 Estrutura do Projeto

```text
AutomacaoFotos/
├── fotos_arapiraca_final/  ← Fotos baixadas (Ignorado no Git)
├── main.py                 ← Orquestrador do sistema
├── scraper_site.py         ← Lógica de navegação e download
├── leitor_html.py          ← Integração com base WinThor
├── validador.py            ← Motor de comparação fuzzy
├── .gitignore              ← Filtro de arquivos para o repositório
├── README.md               ← Documentação do sistema
└── requirements.txt        ← Dependências do projeto
