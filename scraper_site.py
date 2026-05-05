# scraper_site.py
import requests
import re
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

def abrir_menu_categorias(driver, wait):
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Categorias')]")))
        btn.click()
        time.sleep(2)
        return True
    except:
        print("❌ Não conseguiu abrir menu 'Categorias'")
        return False

def clicar_categoria(driver, wait, nome_categoria):
    try:
        link = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{nome_categoria}')]")))
        link.click()
        time.sleep(5)
        return True
    except:
        print(f"❌ Categoria '{nome_categoria}' não encontrada")
        return False

def pegar_primeiro_produto_da_pagina(driver, wait):
    try:
        produto = wait.until(EC.element_to_be_clickable((
            By.XPATH, "(//a[img and (contains(@href, '/product/') or contains(@href, '/produto/'))])[1]"
        )))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", produto)
        time.sleep(1)
        return produto.get_attribute("href")
    except:
        return None

def pegar_proximo_link_produto(driver):
    seletores = [
        "a[rel='next']",
        "a.next",
        "//a[contains(@class, 'next')]",
        "//a[contains(text(), '›') or contains(text(), '>')]"
    ]
    for sel in seletores:
        try:
            if sel.startswith("//"):
                el = driver.find_element(By.XPATH, sel)
            else:
                el = driver.find_element(By.CSS_SELECTOR, sel)
            href = el.get_attribute("href")
            if href and href != driver.current_url:
                return href
        except:
            continue
    return None

def extrair_detalhes(driver, url, wait):
    try:
        driver.get(url)
        time.sleep(3)

        nome = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1.product_title, h1"))).text.strip()

        # AJUSTADO: find_elements para não parar o código se não achar descrição
        desc_els = driver.find_elements(By.CSS_SELECTOR, ".woocommerce-product-details__short-description, .description")
        texto_desc = desc_els[0].text if desc_els else ""

        partes = texto_desc.split(',')
        codigos_encontrados = []
        for parte in partes:
            numeros = re.findall(r'\d+', parte)
            if numeros:
                cod_limpo = str(int(numeros[0]))
                if cod_limpo not in codigos_encontrados and len(cod_limpo) >= 3:
                    codigos_encontrados.append(cod_limpo)

        # AJUSTADO: find_elements para não parar o código se não achar imagem
        img_els = driver.find_elements(By.CSS_SELECTOR, "img.wp-post-image, .woocommerce-product-gallery__image img")
        url_img = ""
        if img_els:
            img_el = img_els[0]
            url_img = img_el.get_attribute("data-src") or img_el.get_attribute("src")
            if url_img and url_img.startswith('//'):
                url_img = 'https:' + url_img
            url_img = url_img.split('?')[0]

        return {'nome': nome, 'codigos': codigos_encontrados, 'url_img': url_img}

    except Exception as e:
        print(f"⚠️ Erro ao extrair detalhes: {e}")
        return None

def salvar_imagem_real(url, caminho):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(caminho, 'wb') as f:
                f.write(r.content)
            return True
    except:
        return False

def salvar_imagem_nao_validada(url_img, codigo, pasta="fotos_nao_validadas"):
    import os
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    
    caminho = os.path.join(pasta, f"{codigo}.jpg")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        r = requests.get(url_img, headers=headers, timeout=15)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(caminho, 'wb') as f:
                f.write(r.content)
            print(f"   📸 Foto salva (não validada): {codigo}.jpg")
            return True
    except:
        return False