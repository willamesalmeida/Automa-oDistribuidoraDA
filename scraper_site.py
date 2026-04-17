# scraper_site.py
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

        # Código do produto (Correção do erro da foto!)
        desc_el = driver.find_element(By.CSS_SELECTOR, ".woocommerce-product-details__short-description")
        texto_desc = desc_el.text # Pega o texto do elemento
        
        numeros = re.findall(r'\d+', texto_desc)
        
        if numeros:
            cod_site = str(int(numeros[0]))
            
            # Foto do produto
            img_el = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".woocommerce-product-gallery__image img")))
            url_img = img_el.get_attribute("data-src") or img_el.get_attribute("src")
            
            if url_img:
                url_img = url_img.split('?')[0]
                if url_img.startswith('//'): url_img = 'https:' + url_img
            
            return {'codigo': cod_site, 'nome': nome, 'url_img': url_img}
            
    except Exception as e:
        print(f"⚠️ Erro no link: {url[:50]}... -> {e}")
        return None
    return None

def salvar_imagem_real(url, caminho):
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://distribuidoraarapiraca.com.br/"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(caminho, 'wb') as f:
                f.write(r.content)
            return True
    except:
        pass
    return False