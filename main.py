# main.py
import leitor_html
import scraper_site
import validador
import os
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import time

def iniciar():
    PASTA_VALIDADAS = "fotos_arapiraca_final"
    PASTA_NAO_VALIDADAS = "fotos_nao_validadas"
    ARQUIVO_ERROS = "nao_encontrados.txt"
    HTML_BASE = "produtosExportados2.html"

    for pasta in [PASTA_VALIDADAS, PASTA_NAO_VALIDADAS]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)

    print("📂 Carregando base WinThor...")
    soup_base = leitor_html.carregar_soup(HTML_BASE)
    if not soup_base:
        print("❌ Não foi possível carregar a base WinThor!")
        return

    driver = scraper_site.configurar_driver()
    wait = WebDriverWait(driver, 25)

    categorias = ["Banheiro"]

    contador_total = 0
    inicio_geral = datetime.now()

    try:
        for categoria in categorias:
            print(f"\n{'='*95}")
            print(f"🔄 CATEGORIA: {categoria.upper()}")
            print(f"{'='*95}\n")

            driver.get("https://distribuidoraarapiraca.com.br/")
            time.sleep(4)

            if not scraper_site.abrir_menu_categorias(driver, wait):
                continue
            if not scraper_site.clicar_categoria(driver, wait, categoria):
                continue

            print(f"✅ Categoria carregada: {categoria}\n")

            link_atual = scraper_site.pegar_primeiro_produto_da_pagina(driver, wait)

            while link_atual:
                contador_total += 1

                p = scraper_site.extrair_detalhes(driver, link_atual, wait)

                if p and p.get('codigos'):
                    nome_site = p['nome']
                    lista_codigos = p['codigos']
                    url_img = p.get('url_img')

                    # SAÍDA LIMPA E ORGANIZADA
                    print(f"[{contador_total}] {link_atual}")
                    print(f"   Produto do Site : {nome_site}")

                    validado_algum = False

                    for cod in lista_codigos:
                        nome_winthor = leitor_html.buscar_produto_na_base(soup_base, cod)

                        if nome_winthor:
                            passou, score = validador.validar_produto(nome_site, nome_winthor)

                            print(f"   Produto da Base : {nome_winthor}")
                            print(f"   Similaridade    : {int(score)}%")

                            if passou:
                                caminho = os.path.join(PASTA_VALIDADAS, f"{cod}.jpg")
                                if scraper_site.salvar_imagem_real(url_img, caminho):
                                    print(f"   ✅ STATUS: VALIDADO com {int(score)}% de similaridade")
                                    print(f"      Foto salva como: {cod}.jpg")
                                validado_algum = True
                            else:
                                print(f"   ⚠️  STATUS: Similaridade baixa ({int(score)}%)")
                                scraper_site.salvar_imagem_nao_validada(url_img, cod, PASTA_NAO_VALIDADAS)
                        else:
                            print(f"   ❌ STATUS: Código {cod} não encontrado na base")
                            with open(ARQUIVO_ERROS, "a", encoding="utf-8") as f:
                                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | Código: {cod} | Nome Site: {nome_site} | Link: {link_atual}\n")
                            scraper_site.salvar_imagem_nao_validada(url_img, cod, PASTA_NAO_VALIDADAS)

                    if not validado_algum and url_img and lista_codigos:
                        print(f"   📁 Produto salvo na pasta de não validados")

                else:
                    print(f"[{contador_total}] ⚠️ Erro ao extrair dados do produto")

                print("-" * 95)

                # Próximo produto
                link_atual = scraper_site.pegar_proximo_link_produto(driver)
                if not link_atual:
                    print(f"🛑 Fim da categoria '{categoria}'.\n")
                    break

                time.sleep(2)

    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

    finally:
        driver.quit()
        duracao = datetime.now() - inicio_geral
        print(f"\n{'='*95}")
        print("🏁 PROCESSO FINALIZADO")
        print(f"⏱  Duração total       : {duracao}")
        print(f"📦 Produtos processados : {contador_total}")
        print(f"✅ Fotos validadas      → fotos_arapiraca_final")
        print(f"📁 Fotos não validadas  → fotos_nao_validadas")
        print(f"📄 Erros registrados    → {ARQUIVO_ERROS}")
        print(f"{'='*95}")


if __name__ == "__main__":
    iniciar()