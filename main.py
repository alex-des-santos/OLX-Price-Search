from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import time
import random
import csv
import statistics

def inicializar_driver(driver_path):
    service = EdgeService(executable_path=driver_path)
    options = webdriver.EdgeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    return webdriver.Edge(service=service, options=options)

def extrair_precos_e_links(driver):
    anuncios_extracao = []
    ignorados = []
    try:
        # Aguarda que os anúncios sejam carregados
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'section[data-ds-component="DS-AdCard"]'))
        )
        # Seleciona os elementos que contêm os anúncios
        anuncios = driver.find_elements(By.CSS_SELECTOR, 'section[data-ds-component="DS-AdCard"]')
        print(f"Encontrados {len(anuncios)} anúncios.")

        for anuncio in anuncios:
            try:
                # Extrai o título do anúncio
                titulo_elemento = anuncio.find_element(By.CSS_SELECTOR, 'h2.olx-ad-card__title')
                titulo = titulo_elemento.text.strip()
                if not titulo:
                    print("Anúncio com título vazio ignorado.")
                    ignorados.append("Título vazio")
                    continue

                print(f"Título do anúncio: {titulo}")

                # Filtrar anúncios irrelevantes
                if '3090' not in titulo or any(excluir in titulo for excluir in ['3080', '4070']):
                    ignorados.append(titulo)
                    continue

                # Extrai o preço do anúncio
                elemento_preco = anuncio.find_element(By.CSS_SELECTOR, 'h3.olx-ad-card__price')
                texto_preco = elemento_preco.text
                preco = re.sub(r'[^\d]', '', texto_preco)
                if not preco:
                    continue

                # Extrai o link do anúncio
                elemento_link = anuncio.find_element(By.CSS_SELECTOR, 'a.olx-ad-card__link-wrapper')
                link = elemento_link.get_attribute('href')

                anuncios_extracao.append({'titulo': titulo, 'preco': int(preco), 'link': link})

            except NoSuchElementException:
                print("Elemento esperado não encontrado em um anúncio.")
                ignorados.append("Elemento não encontrado")
    except TimeoutException:
        print("Timeout ao esperar pelos anúncios.")
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
    return anuncios_extracao, ignorados

def navegar_para_olx(driver, url):
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("Navegação bem-sucedida para olx.com.br")
    except TimeoutException:
        print("Timeout ao esperar o carregamento da página.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def rolar_pagina_ate_fim(driver):
    altura_inicial = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(random.uniform(1, 3))  # Espera aleatória para simular comportamento humano
        altura_atual = driver.execute_script("return document.body.scrollHeight")
        if altura_atual == altura_inicial:
            break
        altura_inicial = altura_atual

def salvar_planilha(anuncios, ignorados):
    try:
        # Salvar anúncios
        with open('anuncios_completos.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Título', 'Preço (R$)', 'Link'])
            for anuncio in anuncios:
                writer.writerow([anuncio['titulo'], anuncio['preco'], anuncio['link']])
        print("Anúncios completos salvos em anuncios_completos.csv")

        # Salvar anúncios ignorados
        with open('anuncios_ignorados.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Título Ignorado'])
            writer.writerows([[anuncio] for anuncio in ignorados])
        print("Anúncios ignorados salvos em anuncios_ignorados.csv")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

def remover_outliers(precos):
    if len(precos) < 2:
        return precos  # Sem outliers para remover
    media = statistics.mean(precos)
    desvio_padrao = statistics.stdev(precos)
    return [preco for preco in precos if abs(preco - media) <= 2 * desvio_padrao]

def main():
    driver_path = "S:/Dev/edgedriver_win64/msedgedriver.exe"
    url_base = "https://www.olx.com.br/informatica/placas-de-video?q=rtx+3090&opst=2"
    
    driver = inicializar_driver(driver_path)
    
    try:
        anuncios_totais = []
        ignorados_totais = []
        for pagina in range(1, 4):
            url_pagina = f"{url_base}&o={pagina}"
            navegar_para_olx(driver, url_pagina)
            rolar_pagina_ate_fim(driver)
            anuncios, ignorados = extrair_precos_e_links(driver)
            anuncios_totais.extend(anuncios)
            ignorados_totais.extend(ignorados)
        
        # Salvar os anúncios e ignorados em arquivos CSV
        salvar_planilha(anuncios_totais, ignorados_totais)
        
        if anuncios_totais:
            precos = [anuncio['preco'] for anuncio in anuncios_totais]
            maior_preco = max(precos)
            menor_preco = min(precos)
            media_preco = sum(precos) / len(precos)
            print("\nResumo dos preços extraídos:")
            print(f"- Maior preço: R${maior_preco}")
            print(f"- Menor preço: R${menor_preco}")
            print(f"- Média de preços: R${media_preco:.2f}")
            print(f"Total de anúncios processados: {len(anuncios_totais)}")
            print(f"Total de anúncios ignorados: {len(ignorados_totais)}")
        else:
            print("Nenhum anúncio processado.")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
