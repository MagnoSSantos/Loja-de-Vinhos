# Use uma imagem base com Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo de requisitos para dentro do contêiner
COPY requirements.txt requirements.txt

# Instalar as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante da aplicação para o contêiner
COPY . .

# Expor a porta em que a aplicação Flask irá rodar
EXPOSE 5000

# Definir o comando para rodar a aplicação
CMD ["python", "app.py"]
