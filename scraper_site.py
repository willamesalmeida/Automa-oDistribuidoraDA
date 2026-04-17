import requests
import re
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def configurar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # Sugestão de Engenheiro: Rodar em headless se quiser mais velocidade no futuro
    # options.add_argument("--headless") 
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def pegar_proximo_link(driver):
    """Localiza o botão 'Próximo' para navegação infinita"""
    seletores = [
        "a[rel='next']", 
        ".product_navigation a.next", 
        ".woocommerce-product-navigation__next a"
    ]
    for s in seletores:
        try:
            return driver.find_element(By.CSS_SELECTOR, s).get_attribute("href")
        except:
            continue
    return None

def extrair_detalhes(driver, url, wait):
    try:
        driver.get(url)
        time.sleep(2) # Espera o site carregar
        
        # Nome do produto
        nome = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product_title"))).text

        # --- LÓGICA DE MÚLTIPLOS CÓDIGOS (ESTILO WILLAMES) ---
        desc_el = driver.find_element(By.CSS_SELECTOR, ".woocommerce-product-details__short-description")
        texto_desc = desc_el.text 
        
        # 1. Primeiro quebramos pela vírgula
        partes = texto_desc.split(',')
        codigos_encontrados = []

        for parte in partes:
            # 2. Em cada parte, pegamos apenas os números (limpeza forense)
            numeros = re.findall(r'\d+', parte)
            if numeros:
                # 3. Pegamos o primeiro grupo de números de cada parte e limpamos
                cod_limpo = str(int(numeros[0]))
                if cod_limpo not in codigos_encontrados:
                    codigos_encontrados.append(cod_limpo)
        
        # Se encontrou ao menos um código, prossegue para a foto
        if codigos_encontrados:
            # Foto do produto
            img_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".woocommerce-product-gallery__image img")))
            url_img = img_el.get_attribute("data-src") or img_el.get_attribute("src")
            
            if url_img:
                url_img = url_img.split('?')[0]
                if url_img.startswith('//'): url_img = 'https:' + url_img
            
            # AGORA RETORNAMOS UMA LISTA DE CÓDIGOS
            return {'codigos': codigos_encontrados, 'nome': nome, 'url_img': url_img}
            
    except Exception as e:
        print(f"⚠️ Erro no link: {url[:50]}... -> {e}")
        return None
    return None

def salvar_imagem_real(url, caminho):
    # Proteção de Header para simular navegador real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://distribuidoraarapiraca.com.br/"
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        # Verificamos se o download é válido (> 1KB para evitar arquivos corrompidos)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(caminho, 'wb') as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"❌ Erro ao salvar imagem: {e}")
    return False