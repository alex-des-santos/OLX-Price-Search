import os
import gradio as gr
import pandas as pd
import webbrowser
from scraper import buscar_anuncios

# Armazena os resultados completos após a busca
resultados_completos = pd.DataFrame()

def make_clickable(url):
    return f'<a href="{url}" target="_blank">{url}</a>'

# Função de interface para exibir resultados paginados
def interface(item_procurado):
    global resultados_completos
    mensagem, tabela, maior_preco, menor_preco, media_preco = buscar_anuncios(item_procurado)
    # Aqui estamos lendo novamente o HTML. Isso remove formatações HTML.
    resultados_completos = pd.read_html(tabela, flavor="html5lib")[0]
    
    # No scraper.py, a coluna final de links é "Link do Anúncio".
    # Após o pd.read_html(), a formatação <a> é perdida, ficando apenas o texto do link.
    # Portanto, precisamos reaplicar a formatação clicável.
    if "Link do Anúncio" in resultados_completos.columns:
        resultados_completos["Link do Anúncio"] = resultados_completos["Link do Anúncio"].apply(make_clickable)

    return mensagem, exibir_pagina(1), maior_preco, menor_preco, media_preco

# Função para exibir uma página específica
def exibir_pagina(pagina, itens_por_pagina=10):
    global resultados_completos
    inicio = (pagina - 1) * itens_por_pagina
    fim = inicio + itens_por_pagina
    pagina_resultados = resultados_completos.iloc[inicio:fim]
    return pagina_resultados.to_html(escape=False, index=False)

# Função para exportar os resultados para CSV
def exportar_csv():
    global resultados_completos
    resultados_completos.to_csv("resultados.csv", index=False)
    return "resultados.csv"

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
    
    tabela_links = gr.HTML(label="Anúncios Encontrados")
    
    # Controles para navegação por páginas
    with gr.Row():
        pagina_atual = gr.Number(value=1, label="Página", interactive=True)
        botao_pagina = gr.Button("Exibir Página")
    
    # Botão para exportar resultados
    botao_exportar = gr.Button("Exportar para CSV")
    link_download = gr.File(label="Baixar CSV")

    # Ações dos botões
    botao_buscar.click(
        interface,
        inputs=item_input,
        outputs=[resumo, tabela_links, maior_preco, menor_preco, media_preco]
    )

    botao_pagina.click(
        exibir_pagina,
        inputs=pagina_atual,
        outputs=tabela_links
    )

    botao_exportar.click(
        exportar_csv,
        outputs=link_download
    )

# Auto-lançamento da interface
port = int(os.environ.get("PORT", 7878))
demo.launch(server_port=port, server_name="0.0.0.0")