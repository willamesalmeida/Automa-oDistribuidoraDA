import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

# Carrega credenciais do arquivo .env
load_dotenv()

def iniciar_upload_maxima(caminho_pasta_fotos):
    usuario_env = os.getenv("MAXIMA_USER")
    senha_env = os.getenv("MAXIMA_PASS")

    # 1. Configuração do Driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)

    try:
        # --- ETAPA 1: LOGIN (MANTIDA) ---
        print("🌍 Acessando o portal...")
        driver.get("https://app.solucoesmaxima.com.br/login")
        
        print("⏳ Preenchendo login...")
        user_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='user'], input[id='user'], input[placeholder*='Usuário']")))
        user_field.clear()
        user_field.send_keys(usuario_env)
        
        pass_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        pass_field.clear()
        pass_field.send_keys(senha_env)
        
        btn_entrar = driver.find_element(By.XPATH, "//button[contains(., 'Entrar')]")
        driver.execute_script("arguments[0].click();", btn_entrar)
        print("✅ Login efetuado!")

        # --- ETAPA 2: CLIQUE NO CARD DE PEDIDO (MANTIDA) ---
        print("⏳ Aguardando carregamento dos módulos (Angular)...")
        time.sleep(5) 

        print("🎯 Tentando clicar no card de PEDIDOS...")
        try:
            xpath_card = "//mat-card[.//div[contains(text(), 'PEDIDO')]]"
            card_pedido = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_card)))
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card_pedido)
            time.sleep(1)
            
            actions = ActionChains(driver)
            actions.move_to_element(card_pedido).click().perform()
            print("✅ Clique no card realizado!")
            
        except Exception as e:
            print(f"⚠️ Falha no clique principal, tentando clique forçado: {e}")
            driver.execute_script("document.querySelector('mat-card.mat-mdc-card').click();")

        # --- ETAPA 3: MUDANÇA DE ABA (MANTIDA) ---
        print("⏳ Verificando abertura do sistema em nova aba...")
        time.sleep(5)
        
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            print(f"🔗 Aba alterada com sucesso!")
        else:
            print("❌ Erro: A aba de pedidos não abriu.")
            return

        # --- ETAPA 4: NAVEGAÇÃO NO MENU LATERAL (MANTIDA) ---
        print("📂 Localizando o botão Extra no menu lateral...")
        time.sleep(8) 

        try:
            icone_extra = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "em.la-plus-circle")))
            actions = ActionChains(driver)
            actions.move_to_element(icone_extra).perform()
            print("🖱️ Mouse posicionado sobre o ícone! Aguardando expansão...")
            time.sleep(2) 

            xpath_extras = "//a[contains(@class, 'm-menu__link')]//span[contains(text(), 'Extras')]/ancestor::a"
            btn_extra = driver.find_element(By.XPATH, xpath_extras)
            driver.execute_script("arguments[0].click();", btn_extra)
            print("✅ Menu Extras ativado e clicado!")

        except Exception as e:
            print(f"⚠️ Erro no hover, tentando clique forçado direto no ícone: {e}")
            btn_fallback = driver.find_element(By.CSS_SELECTOR, "em.la-plus-circle")
            driver.execute_script("arguments[0].click();", btn_fallback)
        
        print("📸 Abrindo tela de Upload Rápido...")
        link_upload = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'fotos-produto/rapido')]")))
        driver.execute_script("arguments[0].click();", link_upload)

        # --- ETAPA 5: UPLOAD DE ARQUIVOS (MÉTODO DIRETO PELO INPUT) ---
        print("📂 Localizando campo de upload oculto...")
        
        # Identifica o input oculto que você encontrou no console
        input_file = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][filedrop]")))

        # Prepara a lista de caminhos de arquivos na pasta
        caminho_pasta = os.path.abspath(caminho_pasta_fotos)
        extensoes_validas = ('.png', '.jpg', '.jpeg')
        arquivos = [os.path.join(caminho_pasta, f) for f in os.listdir(caminho_pasta) if f.lower().endswith(extensoes_validas)]
        
        if arquivos:
            # Junta os caminhos com \n para enviar múltiplos arquivos de uma vez
            caminhos_unidos = "\n".join(arquivos)
            
            print(f"📤 Enviando {len(arquivos)} arquivos diretamente para o input...")
            # Envia diretamente para o elemento, sem precisar clicar no botão azul
            input_file.send_keys(caminhos_unidos)
            print("✅ Arquivos carregados na fila do navegador!")
        else:
            print("⚠️ Nenhuma foto válida encontrada na pasta.")

        # --- ETAPA 6: FINALIZAÇÃO ---
        print("⏳ Aguardando processamento das miniaturas...")
        
        # O botão 'Upload!' aparece após as fotos serem processadas pelo site
        btn_final = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Upload!')]")))
        
        time.sleep(2) # Pausa para garantir o processamento
        driver.execute_script("arguments[0].click();", btn_final)
        print("🚀 SUCESSO: Fotos enviadas para a Distribuidora Arapiraca!")

    except Exception as e:
        print(f"🚨 Ocorreu um erro: {e}")
    finally:
        print("🏁 Fim do processo.")

if __name__ == "__main__":
    PASTA = "./fotos_arapiraca_final"
    if os.path.exists(PASTA):
        iniciar_upload_maxima(PASTA)
    else:
        print(f"❌ Pasta '{PASTA}' não encontrada!")