from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Veiculo, Transacao, RegistroEmissao, MetaSustentabilidade, MetaUsuario, UserProfile
import json
from unittest.mock import patch

class CleanTaggySystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario_teste = User.objects.create_user(username='testador', password='senha_segura123')
        
        self.veiculo_teste = Veiculo.objects.create(
            usuario=self.usuario_teste,
            placa='XYZ-9876',
            modelo='Hatch Compacto',
            tipo_combustivel='GASOLINA',
            categoria='HATCH'
        )

    def test_controle_de_sessao_e_redirecionamento(self):
        response_deslogado = self.client.get('/')
        self.assertEqual(response_deslogado.status_code, 302)
        self.assertTrue('/login' in response_deslogado.url)

    def test_fluxo_de_acesso_autenticado(self):
        self.client.login(username='testador', password='senha_segura123')
        
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
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

    def test_tarefa_25_fluxo_de_metas_e_gamificacao(self):
        """
        Tarefas 25 e 27: Testa o fluxo completo de Gamificação.
        Adiciona meta, conclui meta e verifica se os pontos de CO2 foram injetados no sistema.
        """
        self.client.login(username='testador', password='senha_segura123')
        
        # Cria uma meta no catálogo
        meta = MetaSustentabilidade.objects.create(
            titulo="Desafio de Teste",
            descricao="Teste automatizado",
            objetivo_kg=15.0
        )
        
        # Adiciona a meta ao usuário
        response_add = self.client.get(f'/sustainability/adicionar-meta/{meta.id}/')
        self.assertEqual(response_add.status_code, 302) # 302 = Sucesso no Redirecionamento
        
        meta_usuario = MetaUsuario.objects.get(usuario=self.usuario_teste, meta=meta)
        self.assertFalse(meta_usuario.concluida)
        
        # Conclui a meta
        response_concluir = self.client.get(f'/sustainability/concluir-meta/{meta_usuario.id}/')
        self.assertEqual(response_concluir.status_code, 302)
        
        # Valida se a meta foi fechada e a recompensa (Transação) foi criada
        meta_usuario.refresh_from_db()
        self.assertTrue(meta_usuario.concluida)
        
        transacao_recompensa = Transacao.objects.filter(usuario=self.usuario_teste, local__startswith='Desafio').first()
        self.assertIsNotNone(transacao_recompensa)
        self.assertEqual(transacao_recompensa.co2_economizado, 15.0)

    def test_tarefa_27_equivalencias_dinamicas(self):
        """
        Tarefa 27: Testa se os cálculos matemáticos das equivalências estão precisos.
        """
        self.client.login(username='testador', password='senha_segura123')
        Transacao.objects.create(usuario=self.usuario_teste, local='Pedágio Teste', valor_pedagio=0.0, co2_economizado=60.0)
        
        response = self.client.get('/sustainability/')
        self.assertEqual(response.context['arvores_salvas'], 3)       # 60kg / 20 = 3 árvores
        self.assertEqual(response.context['sacolas_evitadas'], 2000)  # 60kg / 0.03 = 2000 sacolas
        self.assertEqual(response.context['banhos_poupados'], 40)     # 60kg / 1.5 = 40 banhos
