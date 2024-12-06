import gradio as gr
import webbrowser
from scraper import buscar_anuncios  # Importa a função principal do scraper

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
    
    tabela_links = gr.HTML(label="Anúncios Encontrados")
    
    botao_buscar.click(
        interface,
        inputs=item_input,
        outputs=[resumo, tabela_links, maior_preco, menor_preco, media_preco]
    )

# Auto-lançamento da interface
url = "http://0.0.0.0:7878"  # Alteração para permitir acesso externo
webbrowser.open(url)
demo.launch(server_port=7878, server_name="0.0.0.0")  # Alteração do server_name para '0.0.0.0'