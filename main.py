import leitor_html
import scraper_site
import validador
import os
from selenium.webdriver.support.ui import WebDriverWait

def iniciar():
    PASTA_FOTOS = "fotos_arapiraca_final"
    ARQUIVO_ERROS = "nao_encontrados.txt"
    HTML_BASE = "produtosExportados2.html" 
    
    # Link de partida
    link_atual = "https://distribuidoraarapiraca.com.br/product/2-interruptor-paralelo-10a-250v-c-placa-apoio/"
    
    if not os.path.exists(PASTA_FOTOS): 
        os.makedirs(PASTA_FOTOS)

    print("📂 Abrindo base WinThor...")
    soup_base = leitor_html.carregar_soup(HTML_BASE)
    if not soup_base: 
        return

    driver = scraper_site.configurar_driver()
    wait = WebDriverWait(driver, 20)
    
    contador = 0
    
    try:
        while link_atual:
            contador += 1
            print(f"\n🚀 [{contador}] Acessando: {link_atual}")
            
            p = scraper_site.extrair_detalhes(driver, link_atual, wait)
            
            if p:
                nome_s = p['nome']
                lista_codigos = p['codigos'] # Agora recebemos uma lista!

                print(f"📦 Produto Site: {nome_s}")
                print(f"🔢 Códigos detectados: {', '.join(lista_codigos)}")

                # O Robô agora itera sobre cada código encontrado no produto
                for cod in lista_codigos:
                    print(f"\n🔍 Validando código individual: {cod}")
                    
                    nome_w = leitor_html.buscar_produto_na_base(soup_base, cod)

                    if nome_w:
                        # Validação Fuzzy
                        passou, score = validador.validar_produto(nome_s, nome_w)
                        
                        print(f"   BASE WINTHOR: {nome_w}")
                        print(f"   SIMILARIDADE: {int(score)}%")

                        if passou:
                            print(f"   ✅ VALIDADO! Salvando foto para o código {cod}...")
                            caminho = os.path.join(PASTA_FOTOS, f"{cod}.jpg")
                            
                            if scraper_site.salvar_imagem_real(p['url_img'], caminho):
                                print(f"   📸 Foto salva com sucesso.")
                        else:
                            print(f"   ⚠️ DIVERGENTE! (Abaixo da margem)")
                    else:
                        print(f"   ❌ CÓDIGO {cod} NÃO ENCONTRADO NO WINTHOR.")
                        with open(ARQUIVO_ERROS, "a", encoding="utf-8") as f:
                            f.write(f"Código: {cod} | Nome Site: {nome_s} | Link: {link_atual}\n")
            
            # Navegação Infinita
            link_atual = scraper_site.pegar_proximo_link(driver)
            
            if not link_atual:
                print("\n🏁 Fim da linha. Não há mais botões de 'Próximo'.")
                break

    finally:
        driver.quit()
        print("\n🏁 Processo finalizado com sucesso!")

if __name__ == "__main__":
    iniciar()