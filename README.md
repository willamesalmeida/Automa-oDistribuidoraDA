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
└── requirements.txt        ← Dependências do projeto ```
```

## 🚀 Como Executar
Requisitos
Python 3.12 ou superior

Google Chrome instalado

Arquivo produtosExportados2.html (base WinThor) na raiz do projeto

Instalação
Clone o repositório:

Bash
git clone [https://github.com/seu-usuario/AutomacaoFotosDA.git](https://github.com/seu-usuario/AutomacaoFotosDA.git)
cd AutomacaoFotosDA
Crie e ative o ambiente virtual:

Bash
python -m venv venv
venv\Scripts\activate
Instale as dependências:

Bash
pip install -r requirements.txt
Execute o sistema:

Bash
python main.py

## 📌 Funcionalidades Implementadas

[x] Extração de nomes, códigos e URLs de imagem

[x] Tratamento de Lazy Load (data-src)

[x] Validação de similaridade (Margem configurável de 50%)

[x] Download automático e renomeação por SKU

[x] Relatório em tempo real (Sucessos, Erros, Divergências)

[x] Lógica de tratamento de múltiplos códigos por produto

[x] Navegação híbrida (Setas laterais e categorias)


## ⚖️ Licença e Direitos Autorais
Copyright (c) 2026 DA Distribuidora Arapiraca Todos os direitos reservados.

Este software é propriedade exclusiva da DA Distribuidora Arapiraca. É estritamente proibido copiar, modificar, distribuir ou utilizar este software, no todo ou em parte, sem autorização prévia e por escrito da DA Distribuidora Arapiraca.

Este sistema foi desenvolvido para uso interno exclusivo. Qualquer uso não autorizado estará sujeito às penalidades previstas na Lei nº 9.610/1998 (Lei de Direitos Autorais) e demais legislações aplicáveis.

## 👨‍💻 Desenvolvedor
### José Willames de Almeida Barbosa - Engenheiro de Software 
* TI — DA Distribuidora Arapiraca 
* 🎓 Formado em Ciência da Computação 
* 🎓 Pós-graduando em Segurança da Informação e Análise Forense 
* 📍 Arapiraca, Alagoas — Brasil
