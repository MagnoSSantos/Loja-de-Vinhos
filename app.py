from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

# Inicializando a aplicação Flask
app = Flask(__name__)

# Configuração do banco de dados SQLite (o arquivo será criado no mesmo diretório do código)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vinhos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando a extensão SQLAlchemy
db = SQLAlchemy(app)

# Modelo da tabela "vinhos" no banco de dados
class Vinho(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(80), nullable=False)
    categoria = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    about_wine = db.Column(db.String(200), nullable=False)

# Criar o banco de dados com a tabela "vinhos"
with app.app_context():
    db.create_all()

# Rota para listar todos os vinhos
@app.route('/vinhos', methods=['GET'])
def listar_vinhos():
    vinhos = Vinho.query.all()  # Obtém todos os vinhos do banco de dados
    resultado = [{
        'id': vinho.id,
        'nome': vinho.nome,
        'categoria': vinho.categoria,
        'ano': vinho.ano,
        'preco': vinho.preco,
        'about_wine': vinho.about_wine
    } for vinho in vinhos]
    return jsonify(resultado)

# Rota para adicionar um novo vinho
@app.route('/vinhos', methods=['POST'])
def adicionar_vinho():
    if not request.json or 'nome' not in request.json:
        abort(400, description="O nome é obrigatório.")
    
    novo_vinho = Vinho(
        nome=request.json['nome'],
        categoria=request.json['categoria'],
        ano=request.json['ano'],
        preco=request.json['preco'],
        about_wine=request.json['about_wine']
    )
    db.session.add(novo_vinho)  # Adiciona o novo vinho ao banco de dados
    db.session.commit()  # Salva as alterações
    
    return jsonify({
        'id': novo_vinho.id,
        'nome': novo_vinho.nome,
        'categoria': novo_vinho.categoria,
        'ano': novo_vinho.ano,
        'preco': novo_vinho.preco,
        'about_wine': novo_vinho.about_wine
    }), 201  # Retorna o vinho criado com status 201

# Rota para obter um vinho específico pelo ID
@app.route('/vinhos/<int:id>', methods=['GET'])
def obter_vinho(id):
    vinho = Vinho.query.get(id)  # Busca o vinho pelo ID
    if vinho is None:
        abort(404, description="Vinho não encontrado.")
    
    return jsonify({
        'id': vinho.id,
        'nome': vinho.nome,
        'categoria': vinho.categoria,
        'ano': vinho.ano,
        'preco': vinho.preco,
        'about_wine': vinho.about_wine
    })

# Rota para atualizar um vinho existente
@app.route('/vinhos/<int:id>', methods=['PUT'])
def atualizar_vinho(id):
    vinho = Vinho.query.get(id)
    if vinho is None:
        abort(404, description="Vinho não encontrado.")
    
    if not request.json:
        abort(400)
    
    vinho.nome = request.json.get('nome', vinho.nome)
    vinho.categoria = request.json.get('categoria', vinho.categoria)
    vinho.ano = request.json.get('ano', vinho.ano)
    vinho.preco = request.json.get('preco', vinho.preco)
    vinho.about_wine = request.json.get('about_wine', vinho.about_wine)
    
    db.session.commit()  # Salva as alterações no banco de dados
    
    return jsonify({
        'id': vinho.id,
        'nome': vinho.nome,
        'categoria': vinho.categoria,
        'ano': vinho.ano,
        'preco': vinho.preco,
        'about_wine': vinho.about_wine
    })

# Rota para deletar um vinho pelo ID
@app.route('/vinhos/<int:id>', methods=['DELETE'])
def deletar_vinho(id):
    vinho = Vinho.query.get(id)
    if vinho is None:
        abort(404, description="Vinho não encontrado.")
    
    db.session.delete(vinho)
    db.session.commit()
    
    return '', 204  # Sem conteúdo após deletar

# Função principal para rodar o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
