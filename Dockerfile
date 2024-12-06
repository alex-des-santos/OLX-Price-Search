# Use uma imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instale dependências de sistema e limpe caches
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    unzip \
    chromium \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libxi6 \
    libatk1.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgbm-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instale o Chromedriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Adicione /usr/local/bin ao PATH
ENV PATH="/usr/local/bin:${PATH}"

# Copie o arquivo de dependências para o container
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Atualize o Selenium para a versão mais recente
RUN pip install --upgrade selenium

# Copie todo o projeto para o container
COPY . .

# Exponha a porta usada pelo Gradio
EXPOSE 7878

# Comando para executar o aplicativo
CMD ["python", "app/main.py"]
