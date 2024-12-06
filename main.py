import gradio as gr
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re
import statistics
import time
import random


def inicializar_driver(driver_path):
    service = EdgeService(executable_path=driver_path)
    options = webdriver.EdgeOptions()
    options.add_argument('--headless')  # Para rodar sem abrir o navegador
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
    return webdriver.Edge(service=service, options=options)


def extrair_precos_e_links(driver, termo_pesquisa, paginas=3):
    anuncios_totais = []
    ignorados_totais = []
    url_base = f"https://www.olx.com.br/informatica?q={termo_pesquisa.replace(' ', '+')}&opst=2"
    
    for pagina in range(1, paginas + 1):
        url_pagina = f"{url_base}&o={pagina}"
        try:
            driver.get(url_pagina)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            rolar_pagina_ate_fim(driver)

            anuncios, ignorados = extrair_anuncios(driver)
            anuncios_totais.extend(anuncios)
            ignorados_totais.extend(ignorados)
        except Exception as e:
            print(f"Erro na página {pagina}: {e}")
    
    return anuncios_totais


def extrair_anuncios(driver):
    anuncios_extracao = []
    ignorados = []
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'section[data-ds-component="DS-AdCard"]'))
        )
        anuncios = driver.find_elements(By.CSS_SELECTOR, 'section[data-ds-component="DS-AdCard"]')
        
        for anuncio in anuncios:
            try:
                titulo_elemento = anuncio.find_element(By.CSS_SELECTOR, 'h2.olx-ad-card__title')
                titulo = titulo_elemento.text.strip()
                if not titulo:
                    ignorados.append("Título vazio")
                    continue

                elemento_preco = anuncio.find_element(By.CSS_SELECTOR, 'h3.olx-ad-card__price')
                texto_preco = elemento_preco.text
                preco = re.sub(r'[^\d]', '', texto_preco)
                if not preco:
                    continue

                elemento_link = anuncio.find_element(By.CSS_SELECTOR, 'a.olx-ad-card__link-wrapper')
                link = elemento_link.get_attribute('href')

                anuncios_extracao.append({'titulo': titulo, 'preco': int(preco), 'link': link})
            except NoSuchElementException:
                ignorados.append("Elemento não encontrado")
    except TimeoutException:
        pass
    except Exception as e:
        print(f"Erro ao extrair dados: {e}")
    
    return anuncios_extracao, ignorados


def rolar_pagina_ate_fim(driver):
    altura_inicial = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(random.uniform(1, 2))
        altura_atual = driver.execute_script("return document.body.scrollHeight")
        if altura_atual == altura_inicial:
            break
        altura_inicial = altura_atual


def remover_outliers(precos):
    if len(precos) < 2:
        return precos
    media = statistics.mean(precos)
    desvio_padrao = statistics.stdev(precos)
    return [preco for preco in precos if abs(preco - media) <= 2 * desvio_padrao]


def buscar_anuncios(item_procurado):
    driver_path = "S:/Dev/edgedriver_win64/msedgedriver.exe"  # Atualize com o caminho do seu driver
    driver = inicializar_driver(driver_path)
    try:
        anuncios = extrair_precos_e_links(driver, item_procurado)
        if not anuncios:
            return "Nenhum anúncio encontrado.", [], "N/A", "N/A", "N/A"
        
        precos = [anuncio['preco'] for anuncio in anuncios]
        maior_preco = max(precos)
        menor_preco = min(precos)
        media_preco = sum(precos) / len(precos)

        links_formatados = [
            f"R${anuncio['preco']} - [Link do Anúncio]({anuncio['link']})"
            for anuncio in anuncios
        ]
        
        return (
            f"Encontrados {len(anuncios)} anúncios para '{item_procurado}'",
            links_formatados,
            f"R${maior_preco}",
            f"R${menor_preco}",
            f"R${media_preco:.2f}"
        )
    finally:
        driver.quit()


# Configuração da Interface Gradio
def interface(item_procurado):
    return buscar_anuncios(item_procurado)


with gr.Blocks() as demo:
    gr.Markdown("# Busca de Anúncios na OLX")
    
    with gr.Row():
        item_input = gr.Textbox(label="Item a pesquisar", placeholder="Digite o item desejado, ex: RTX 3090")
        botao_buscar = gr.Button("Pesquisar")
    
    with gr.Row():
        resumo = gr.Textbox(label="Resumo da Busca", interactive=False)
    
    with gr.Row():
        maior_preco = gr.Textbox(label="Maior Preço", interactive=False)
        menor_preco = gr.Textbox(label="Menor Preço", interactive=False)
        media_preco = gr.Textbox(label="Preço Médio", interactive=False)
    
    lista_links = gr.Textbox(label="Links e Preços", lines=10, interactive=False)
    
    botao_buscar.click(
        interface,
        inputs=item_input,
        outputs=[resumo, lista_links, maior_preco, menor_preco, media_preco]
    )

demo.launch()
