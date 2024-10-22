# Usar uma imagem base do Python
FROM python:3.10-slim

# Instalar dependências do sistema para o MySQL
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar os arquivos necessários para dentro do contêiner
COPY requirements.txt requirements.txt
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta usada pela aplicação Flask
EXPOSE 5000

# Variáveis de ambiente para a aplicação Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para rodar a aplicação
CMD ["flask", "run"]




