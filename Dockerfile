# 1. Imagem base com Python
# Usar uma imagem 'slim' para manter o tamanho menor
FROM python:3.9-slim

# 2. Instalar o Google Chrome e dependências do sistema
# Necessário para o Selenium funcionar em modo headless
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    --no-install-recommends \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# 4. Copiar o arquivo de dependências e instalar
# Copiar primeiro para aproveitar o cache do Docker se as dependências não mudarem
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar o resto do código da aplicação
COPY . .

# 6. Comando para iniciar a aplicação
# Expõe a porta 8000 e inicia o Uvicorn
# O host 0.0.0.0 é essencial para que a aplicação seja acessível de fora do contêiner
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
