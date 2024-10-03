import unittest
from app import app, db, Vinho  # Importa a aplicação e o banco de dados
from flask import json

class VinhoTestCase(unittest.TestCase):
    
    # Método executado antes de cada teste
    def setUp(self):
        # Define que o Flask usará um banco de dados em memória
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()  # Cria o cliente de teste
        self.app_context = app.app_context()
        self.app_context.push()

        # Cria as tabelas no banco de dados em memória
        db.create_all()
    
    # Método executado após cada teste
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    # Teste para verificar se o endpoint de listar vinhos está funcionando
    def test_listar_vinhos(self):
        # Primeiro, insere um vinho manualmente no banco de dados
        vinho = Vinho(nome="Vinho Teste", categoria="Tinto", ano=2020, preco=50.0, about_wine="Vinho tinto de teste")
        db.session.add(vinho)
        db.session.commit()

        # Faz uma requisição GET para o endpoint /vinhos
        response = self.app.get('/vinhos')
        self.assertEqual(response.status_code, 200)  # Verifica se o status HTTP é 200 (OK)

        # Verifica se o vinho está presente na resposta
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)  # Verifica se há um vinho na resposta
        self.assertEqual(data[0]['nome'], "Vinho Teste")
        self.assertEqual(data[0]['categoria'], "Tinto")
        self.assertEqual(data[0]['ano'], 2020)

    # Teste para adicionar um vinho
    def test_adicionar_vinho(self):
        # Dados para um novo vinho
        novo_vinho = {
            'nome': 'Vinho Branco',
            'categoria': 'Branco',
            'ano': 2019,
            'preco': 60.0,
            'about_wine': 'Vinho branco refrescante'
        }
        
        # Faz uma requisição POST para adicionar o vinho
        response = self.app.post('/vinhos', 
                                 data=json.dumps(novo_vinho), 
                                 content_type='application/json')

        self.assertEqual(response.status_code, 201)  # Verifica se o status HTTP é 201 (Created)
        
        # Verifica se o vinho foi adicionado corretamente no banco de dados
        vinhos = Vinho.query.all()
        self.assertEqual(len(vinhos), 1)
        self.assertEqual(vinhos[0].nome, 'Vinho Branco')

    # Teste para verificar se um vinho pode ser obtido pelo ID
    def test_obter_vinho(self):
        # Primeiro, insere um vinho manualmente no banco de dados
        vinho = Vinho(nome="Vinho Teste", categoria="Tinto", ano=2020, preco=50.0, about_wine="Vinho tinto de teste")
        db.session.add(vinho)
        db.session.commit()

        # Faz uma requisição GET para o endpoint /vinhos/<id>
        response = self.app.get(f'/vinhos/{vinho.id}')
        self.assertEqual(response.status_code, 200)  # Verifica se o status HTTP é 200 (OK)

        # Verifica se o vinho retornado tem os dados corretos
        data = json.loads(response.data)
        self.assertEqual(data['nome'], "Vinho Teste")
        self.assertEqual(data['categoria'], "Tinto")
        self.assertEqual(data['ano'], 2020)

    # Teste para deletar um vinho
    def test_deletar_vinho(self):
        # Primeiro, insere um vinho manualmente no banco de dados
        vinho = Vinho(nome="Vinho a Ser Deletado", categoria="Branco", ano=2018, preco=80.0, about_wine="Vinho para teste de deleção")
        db.session.add(vinho)
        db.session.commit()

        # Faz uma requisição DELETE para o endpoint /vinhos/<id>
        response = self.app.delete(f'/vinhos/{vinho.id}')
        self.assertEqual(response.status_code, 204)  # Verifica se o status HTTP é 200 (OK)

        # Verifica se o vinho foi deletado
        vinho_deletado = db.session.get(Vinho, vinho.id)
        self.assertIsNone(vinho_deletado)  # O vinho deve ser None após ser deletado

if __name__ == '__main__':
    unittest.main()
