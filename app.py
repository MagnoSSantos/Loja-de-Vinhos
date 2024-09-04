from flask import Flask, jsonify, request

# Criar a aplicação Flask
app = Flask(__name__)

# Lista de tarefas (inicialmente vazia)
tasks = []

# Rota para obter todas as tarefas
@app.route('/vinhos', methods=['GET'])
def get_tasks():
    return jsonify(tasks)  # Retorna a lista de tarefas em formato JSON

# Rota para adicionar uma nova tarefa
@app.route('/vinhos', methods=['POST'])
def add_task():
    new_task = request.json  # Obtém os dados da nova tarefa do corpo da requisição
    tasks.append(new_task)   # Adiciona a nova tarefa à lista
    return jsonify(new_task), 201  # Retorna a nova tarefa e um código de status 201 (Criado)

# Função principal para rodar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)  # Roda a aplicação em modo debug


