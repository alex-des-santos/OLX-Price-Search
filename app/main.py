import os
import gradio as gr
import pandas as pd
import webbrowser
from scraper import buscar_anuncios, obter_ufs_disponiveis
import re

# Variável global para armazenar os resultados completos após a busca
resultados_completos = pd.DataFrame()
resultados_originais = pd.DataFrame()  # Nova variável
# Variável global para armazenar UFs disponíveis
ufs_disponiveis = []

def make_clickable(url):
    return f'<a href="{url}" target="_blank">{url}</a>'

# Adicionar nova função de filtro
def filtrar_por_uf(uf_selecionada):
    """Filtra os resultados existentes por UF."""
    global resultados_completos, resultados_originais
    if uf_selecionada == "TODAS":
        resultados_completos = resultados_originais.copy()
    else:
        mask = resultados_originais["Link do Anúncio"].str.contains(f"/{uf_selecionada.lower()}.", case=False, na=False)
        resultados_completos = resultados_originais[mask]
    
    return exibir_pagina(1)

# Função para obter UFs dos resultados
def obter_ufs_dos_resultados(df):
    """Extrai as UFs presentes nos links dos resultados."""
    ufs = set()
    if "Link do Anúncio" in df.columns:
        for link in df["Link do Anúncio"]:
            # Extrai a UF do link (exemplo: https://go.olx.com.br -> GO)
            match = re.search(r'https://([a-z]{2})\.olx\.com\.br', link)
            if match:
                ufs.add(match.group(1).upper())
    return sorted(list(ufs))

# Modificar a função interface para armazenar resultados originais
def interface(item_procurado, uf_selecionada):
    global resultados_completos, resultados_originais
    mensagem, tabela, maior_preco, menor_preco, media_preco, _ = buscar_anuncios(
        item_procurado, 
        uf=None  # Sempre busca todas as UFs
    )
    
    if isinstance(tabela, pd.DataFrame):
        resultados_originais = tabela.copy()
    else:
        # Se tabela é HTML string, usa StringIO
        from io import StringIO
        resultados_originais = pd.read_html(StringIO(tabela), flavor="html5lib")[0]
    
    if "Link do Anúncio" in resultados_originais.columns:
        resultados_originais["Link do Anúncio"] = resultados_originais["Link do Anúncio"].apply(make_clickable)

    # Obter UFs apenas dos resultados encontrados
    ufs_disponiveis = obter_ufs_dos_resultados(resultados_originais)
    
    # Aplica o filtro inicial
    tabela_filtrada = filtrar_por_uf(uf_selecionada)

    # Atualiza o dropdown apenas com as UFs presentes nos resultados
    choices = ["TODAS"] + ufs_disponiveis
    
    return (
        mensagem, 
        tabela_filtrada, 
        maior_preco, 
        menor_preco, 
        media_preco, 
        gr.update(choices=choices, value=uf_selecionada)
    )

def exibir_pagina(pagina):
    global resultados_completos
    if resultados_completos.empty:
        return "Nenhum resultado para exibir."
    
    inicio = (pagina - 1) * 10
    fim = inicio + 10
    return resultados_completos.iloc[inicio:fim].to_html(escape=False, index=False)

# Função para exportar os resultados para CSV
def exportar_csv():
    global resultados_completos
    resultados_completos.to_csv("resultados.csv", index=False)
    return "resultados.csv"

# Modificar a interface Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Busca de Anúncios na OLX")
    
    with gr.Row():
        item_input = gr.Textbox(label="Item a pesquisar", placeholder="Digite o item desejado, ex: RTX 3090")
        uf_dropdown = gr.Dropdown(
            choices=["TODAS"],
            value="TODAS",
            label="UF",
            interactive=True
        )
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
        inputs=[item_input, uf_dropdown],
        outputs=[resumo, tabela_links, maior_preco, menor_preco, media_preco, uf_dropdown]
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

    uf_dropdown.change(
        filtrar_por_uf,
        inputs=[uf_dropdown],
        outputs=[tabela_links]
    )

# Auto-lançamento da interface
port = int(os.environ.get("PORT", 7878))
demo.launch(server_port=port, server_name="0.0.0.0")