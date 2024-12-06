# Use uma imagem oficial do Python como base
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instale dependências de sistema e limpe caches
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
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

# Copie o arquivo de dependências para o container
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o projeto para o container
COPY . .

# Exponha a porta usada pelo Gradio
EXPOSE 7878

# Comando para executar o aplicativo
CMD ["python", "app/main.py"]
