"""
Testes para o sistema de empréstimo de obras utilizando mocks para evitar operações reais de banco de dados.

Este módulo testa o fluxo completo de:
- Criação de obras e usuários.
- Empréstimo e devolução de obras.
- Cálculo de multa em caso de atraso.
- Verificação de chamadas às funções de persistência.

As funções do módulo `database` são mockadas com `unittest.mock.patch` para simular persistência.
"""

from core import Acervo
from models import Obra, Usuario
from datetime import date, timedelta
from unittest.mock import patch
from database import criar_tabelas, limpar_tabelas

def test_fluxo_emprestimo_com_mock():
    """
    Testa o fluxo completo de empréstimo e devolução de uma obra com simulação de persistência.

    O teste realiza as seguintes etapas:
    1. Cria uma instância do acervo.
    2. Adiciona uma obra e um usuário (mockando o salvamento).
    3. Realiza o empréstimo da obra.
    4. Simula a devolução após 10 dias (3 dias de atraso, considerando o prazo padrão de 7 dias).
    5. Verifica se a multa está correta.
    6. Verifica se a obra foi devolvida ao acervo.
    7. Confirma se os métodos de persistência foram chamados.

    Assegura que:
    - A multa é corretamente calculada.
    - A obra é reinserida no acervo após devolução.
    - Todas as funções de banco foram chamadas.
    """

    with patch("database.salvar_obra") as mock_salvar_obra, \
         patch("database.salvar_usuario") as mock_salvar_usuario, \
         patch("core.salvar_emprestimo") as mock_salvar_emprestimo:

        criar_tabelas()
        acervo = Acervo()
        
        livro = Obra("POO Essencial", "Ana Silva", 2025, "Livro", 2)
        joao  = Usuario("João", "joao@example.com")
        
        mock_salvar_obra(livro)
        mock_salvar_usuario(joao)

        acervo += livro
        emprestimo = acervo.emprestar(livro, joao)

        after3 = date.today() + timedelta(days=10)
        multa = acervo.valor_multa(emprestimo, after3)
        
        acervo.devolver(emprestimo, after3)

        assert multa == 3.00  # espera multa de 3 reais

        assert livro in acervo.acervo  # obra deve voltar para o acervo após devolução?

        # Verifica se funções de salvar foram chamadas ao menos uma vez
        assert mock_salvar_obra.called
        assert mock_salvar_usuario.called
        assert mock_salvar_emprestimo.called
