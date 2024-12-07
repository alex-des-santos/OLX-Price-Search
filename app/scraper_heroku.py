import re
import time
import random
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from utils import rolar_pagina_ate_fim


def inicializar_driver():
    """Inicializa o WebDriver Chrome com as configurações corretas para o Heroku."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Executa em modo headless
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/91.0.4472.124 Safari/537.36"
    )
    # Atualize aqui para usar a nova variável de ambiente
    options.binary_location = os.environ.get("CHROME_FOR_TESTING_BIN")

    # Atualize aqui para usar a nova variável de ambiente
    service = ChromeService(executable_path=os.environ.get("CHROMEDRIVER_FOR_TESTING_BIN"))

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def buscar_anuncios(item_procurado):
    """Busca anúncios no OLX e retorna informações formatadas."""
    driver = inicializar_driver()
    try:
        anuncios = extrair_precos_e_links(driver, item_procurado)
        if not anuncios:
            return "Nenhum anúncio encontrado.", pd.DataFrame(), "N/A", "N/A", "N/A"

        precos = [anuncio["preco"] for anuncio in anuncios]
        maior_preco = max(precos)
        menor_preco = min(precos)
        media_preco = sum(precos) / len(precos)

        # Criando DataFrame para exibição formatada
        df_anuncios = pd.DataFrame(anuncios)
        tabela_html = df_anuncios.to_html(escape=False, index=False)

        resumo = f"Foram encontrados {len(anuncios)} anúncios."
        return resumo, tabela_html, f"R$ {maior_preco:.2f}", f"R$ {menor_preco:.2f}", f"R$ {media_preco:.2f}"
    finally:
        driver.quit()


def extrair_precos_e_links(driver, termo_pesquisa, paginas=3):
    """Extrai preços e links de anúncios do OLX."""
    anuncios_totais = []
    url_base = f"https://www.olx.com.br/informatica?q={termo_pesquisa.replace(' ', '+')}&opst=2"

    for pagina in range(1, paginas + 1):
        url_pagina = f"{url_base}&o={pagina}"
        try:
            driver.get(url_pagina)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            rolar_pagina_ate_fim(driver)

            anuncios, _ = extrair_anuncios(driver, termo_pesquisa)
            anuncios_totais.extend(anuncios)
        except Exception as e:
            print(f"Erro na página {pagina}: {e}")

    return anuncios_totais


def extrair_anuncios(driver, termo_pesquisa):
    """Extrai dados de anúncios específicos."""
    anuncios_extracao = []
    ignorados = []
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'section[data-ds-component="DS-AdCard"]'))
        )
        anuncios = driver.find_elements(By.CSS_SELECTOR, 'section[data-ds-component="DS-AdCard"]')

        for anuncio in anuncios:
            try:
                titulo_elemento = anuncio.find_element(By.CSS_SELECTOR, "h2.olx-ad-card__title")
                titulo = titulo_elemento.text.strip()

                if termo_pesquisa.lower() not in titulo.lower():
                    ignorados.append(f"Título ignorado: {titulo}")
                    continue

                elemento_preco = anuncio.find_element(By.CSS_SELECTOR, "h3.olx-ad-card__price")
                texto_preco = elemento_preco.text
                preco = re.sub(r"[^\d]", "", texto_preco)
                if not preco:
                    continue

                elemento_link = anuncio.find_element(By.CSS_SELECTOR, "a.olx-ad-card__link-wrapper")
                link = elemento_link.get_attribute("href")

                anuncios_extracao.append({"preco": int(preco), "link": link})
            except NoSuchElementException:
                ignorados.append("Elemento não encontrado")
    except TimeoutException:
        pass
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")

    return anuncios_extracao, ignorados
