# OLX Price Search

## Descrição
Este projeto é um web scraper que busca e compara preços de produtos no OLX, apresentando os resultados em uma interface web amigável.

## Funcionalidades
- Busca de produtos por nome
- Exibição de preço máximo, mínimo e médio
- Lista de anúncios com links diretos
- Interface web interativa usando Gradio

## Executando com Docker Compose
Você também pode executar o projeto usando Docker Compose. Siga os passos abaixo:

1. Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.
2. Navegue até o diretório do projeto:
    ```bash
    cd OLX-Price-Search
    ```
3. Construa e inicie os containers:
    ```bash
    docker-compose up --build
    ```
4. Após a conclusão da construção, execute:
    ```bash
    docker-compose up -d
    ```
5. Acesse o endereço http://localhost:7878/

## Tecnologias Utilizadas
- Python
- Selenium
- Gradio
- Docker
- Chrome Webdriver

## Como Usar
1. Clone o repositório:
    ```bash
    git clone https://github.com/alex-des-santos/OLX-Price-Search.git
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd OLX-Price-Search
    ```
3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```
4. Execute o script principal:
    ```bash
    python main.py
    ```
5. Acesse o endereço http://localhost:7878/

## Contribuindo
1. Faça um fork do projeto
2. Crie uma branch para sua funcionalidade:
    ```bash
    git checkout -b minha-funcionalidade
    ```
3. Faça commit das suas alterações:
    ```bash
    git commit -m 'Minha nova funcionalidade'
    ```
4. Envie para o repositório remoto:
    ```bash
    git push origin minha-funcionalidade
    ```
5. Abra um Pull Request

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Limitações e Melhorias Futuras
- **Tratamento de Erros:** O scraper pode ser melhorado com um tratamento de erros mais robusto para gerenciar situações como problemas de rede ou mudanças na estrutura do site do OLX.
- **Escalabilidade:** Atualmente, o scraper pode não estar otimizado para lidar com um grande número de buscas simultâneas. Melhorias futuras podem focar em aumentar a escalabilidade e o desempenho.
- **Persistência de Dados:** Considere adicionar um mecanismo para persistir os dados raspados para acesso ou análise offline.
- **Opções de Busca Avançadas:** Expandir as capacidades de busca para incluir filtros (por exemplo, faixa de preço, localização) melhoraria a experiência do usuário.
