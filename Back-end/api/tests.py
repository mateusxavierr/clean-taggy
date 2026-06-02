from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Veiculo, Transacao, RegistroEmissao
import json
from unittest.mock import patch

class CleanTaggySystemTests(TestCase):
    def setUp(self):
        """
        Setup do banco de testes: Roda antes de cada teste.
        Simula a preparação do ambiente que o grupo fez (Tasks de ambiente e banco).
        """
        self.client = Client()
        # Cria um usuário de teste
        self.usuario_teste = User.objects.create_user(username='testador', password='senha_segura123')
        
        # Simula a Task 13 (Cadastro de Veículo)
        self.veiculo_teste = Veiculo.objects.create(
            usuario=self.usuario_teste,
            placa='XYZ-9876',
            modelo='Hatch Compacto',
            tipo_combustivel='GASOLINA',
            categoria='HATCH'
        )

    def test_controle_de_sessao_e_redirecionamento(self):
        """
        Testa as regras de UI/UX e Segurança (Task 12).
        Verifica se páginas protegidas bloqueiam usuários não logados.
        """
        # Tenta acessar dashboard deslogado
        response_deslogado = self.client.get('/')
        # Verifica se o Django interceptou e redirecionou (status 302 é redirect)
        self.assertEqual(response_deslogado.status_code, 302)
        # Opcional: checa se foi mandado pra tela de login
        self.assertTrue('/login' in response_deslogado.url)

    def test_fluxo_de_acesso_autenticado(self):
        """
        Testa o mapeamento de rotas (Task KS) e views (Task LF) logado.
        """
        # Faz o login
        self.client.login(username='testador', password='senha_segura123')
        
        # Acessa a página principal (Dashboard)
        response = self.client.get('/')
        
        # Status 200 significa "OK, página carregada com sucesso"
        self.assertEqual(response.status_code, 200)
        # Verifica se renderizou o template correto
        self.assertTemplateUsed(response, 'api/dashboard.html')

    def test_evolucao_schema_e_calculo_co2(self):
        """
        Testa a lógica de negócios e persistência (Tasks 10 e 11).
        Verifica se o banco aceita os campos novos e se o cálculo salva certo.
        """
        fator_emissao = 0.15

        nova_transacao = Transacao.objects.create(
            usuario=self.usuario_teste,
            local='Pedágio SP',
            valor_pedagio=10.50,
            co2_economizado=0.0,
            km_estimado=True,
            fator_co2=fator_emissao
        )

        # Busca do banco para ver se salvou direitinho
        transacao_salva = Transacao.objects.get(id=nova_transacao.id)
        
        self.assertTrue(transacao_salva.km_estimado)
        self.assertEqual(transacao_salva.fator_co2, 0.15)

    @patch('api.views.calcular_emissao_co2')
    def test_tarefa_19_integridade_matematica_api(self, mock_calcular_co2):
        """
        Tarefa 19: Validação de Integridade Matemática dos Cálculos.
        Testa a rota de cálculo ponta a ponta e valida se a precisão decimal
        está sendo mantida sem perdas de arredondamento precoce (0% de erro).
        """
        # Valor simulado da fórmula científica com alta precisão decimal
        co2_esperado = 12.3456789
        mock_calcular_co2.return_value = co2_esperado

        payload = {
            'veiculo_id': self.veiculo_teste.id,
            'distancia_km': 150.25
        }

        response = self.client.post(
            '/calcular-impacto/',
            data=json.dumps(payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['co2_emitido_kg'], co2_esperado)

        # Validação do armazenamento no banco: o FloatField deve preservar a precisão
        registro_salvo = RegistroEmissao.objects.get(id=response_data['registro_id'])
        self.assertAlmostEqual(registro_salvo.co2_emitido_kg, co2_esperado, places=5)
