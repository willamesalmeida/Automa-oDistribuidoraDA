from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

print("🚀 Iniciando automação corrigida (versão 3)...")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()

wait = WebDriverWait(driver, 25)   # aumentei um pouco o tempo

try:
    driver.get("https://distribuidoraarapiraca.com.br/")
    print("✅ Site aberto")

    # 1. Clica em "Categorias"
    categorias_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Categorias')]"))
    )
    categorias_btn.click()
    print("✅ Menu Categorias aberto")
    time.sleep(2)

    # 2. Clica em "Banheiro"
    banheiro = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Banheiro')]"))
    )
    banheiro.click()
    print("✅ Categoria Banheiro selecionada")

    # Espera longa para a lista de produtos carregar completamente
    time.sleep(6)
    print("✅ Aguardando lista de produtos...")

    # 3. Clica no PRIMEIRO PRODUTO da lista (XPath mais amplo e confiável)
    primeiro_produto = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "(//a[img and (contains(@href, '/product/') or contains(@href, 'produto'))])[1]"
        ))
    )

    # Rolagem para garantir que o elemento esteja visível
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", primeiro_produto)
    time.sleep(1.5)

    primeiro_produto.click()
    print("✅ Primeiro produto clicado com sucesso!")

    time.sleep(6)
    print("🎉 Script finalizado! Você deve estar na página do produto.")

except Exception as e:
    print(f"❌ Erro: {e}")
    print("\n💡 Dica importante:")
    print("   1. Rode o script novamente")
    print("   2. Quando parar no erro, tire um PRINT da tela (página de Banheiro)")
    print("   3. Envie o print aqui para eu ajustar o XPath exato.")

finally:
    input("\nPressione ENTER para fechar o navegador...")
    # driver.quit()