import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

def obter_status_por_nota_fiscal(nota_fiscal_numero: str):
    """
    Realiza o web scraping para obter o status de um pedido a partir do número da nota fiscal.
    """
    # Carrega as credenciais das variáveis de ambiente
    empresa_id = os.getenv("PORTAL_EMPRESA_ID")
    username = os.getenv("PORTAL_USERNAME")
    password = os.getenv("PORTAL_PASSWORD")

    if not all([empresa_id, username, password]):
        return {"error": "As variáveis de ambiente PORTAL_EMPRESA_ID, PORTAL_USERNAME e PORTAL_PASSWORD devem ser definidas."}

    options = webdriver.ChromeOptions()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    options.add_argument(f'user-agent={user_agent}')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    resultado_final = None

    try:
        url_login = "https://portalpostal.com.br/v2/extra/login?returnUrl=%2Fapp"
        driver.get(url_login)
        wait = WebDriverWait(driver, 20)

        # Login com credenciais do .env
        wait.until(EC.presence_of_element_located((By.NAME, "idEmpresa"))).send_keys(empresa_id)
        wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        wait.until(EC.presence_of_element_located((By.ID, "inputSenha"))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Login')]"))).click()

        time.sleep(3)
        url_pesquisa = "https://portalpostal.com.br/v2/app/postagens/pesquisa"
        driver.get(url_pesquisa)

        campo_data_inicio = wait.until(EC.presence_of_element_located((By.NAME, "periodoInicio")))
        campo_data_inicio.clear()
        time.sleep(0.5)
        campo_data_inicio.send_keys("01/01/2025")

        campo_nota_fiscal = wait.until(EC.presence_of_element_located((By.NAME, "notaFiscal")))
        campo_nota_fiscal.clear()
        campo_nota_fiscal.send_keys(nota_fiscal_numero)

        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Pesquisar')]"))).click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody.ui-datatable-data")))
        time.sleep(2)

        linhas_tabela = driver.find_elements(By.CSS_SELECTOR, "tbody.ui-datatable-data > tr")

        if linhas_tabela:
            primeira_linha = linhas_tabela[0]
            link_objeto = primeira_linha.find_element(By.CSS_SELECTOR, "a > b")
            codigo_rastreio = link_objeto.text
            link_objeto.click()

            seletor_status = ".timeline-event .status-badge"
            status_element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, seletor_status)))
            status_atual = status_element.text

            resultado_final = {"codigo_rastreio": codigo_rastreio, "status": status_atual, "nota_fiscal": nota_fiscal_numero}

            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            time.sleep(1)

    except Exception as e:
        print(f"Ocorreu um erro durante a automação: {e}")
        return {"error": str(e)}
    finally:
        driver.quit()

    return resultado_final
