"""import pytest
from datetime import datetime, timedelta
from models import Usuario, Obra, Emprestimo
from core import Acervo

@pytest.fixture
def acervo():
    return Acervo()

@pytest.fixture
def obra():
    return Obra("Dom Casmurro", "Machado de Assis", 1899, "Romance")

@pytest.fixture
def usuario():
    return Usuario("João", "joao@email.com")

def test_adicionar_obra(acervo, obra):
    acervo.adicionar(obra)
    assert obra in acervo.acervo
    assert acervo.acervo[obra] == 1

def test_remover_obra(acervo, obra):
    acervo.adicionar(obra)
    acervo.remover(obra)
    assert obra not in acervo.acervo

def test_emprestar_obra(acervo, obra, usuario):
    acervo.adicionar(obra)
    emprestimo = acervo.emprestar(obra, usuario)
    assert emprestimo.obra == obra
    assert emprestimo.usuario == usuario
    assert obra not in acervo.acervo  # removido após empréstimo

def test_devolver_obra(acervo, obra, usuario):
    acervo.adicionar(obra)
    emprestimo = acervo.emprestar(obra, usuario)
    data_dev = datetime.now().date()
    acervo.devolver(emprestimo, data_dev)
    assert obra in acervo.acervo

def test_valor_multa_zero(acervo, obra, usuario):
    acervo.adicionar(obra)
    emprestimo = acervo.emprestar(obra, usuario)
    hoje = emprestimo.previsao  # devolver no prazo
    acervo.valor_multa(emprestimo, hoje)
    assert usuario.divida == 0

def test_valor_multa_atraso(acervo, obra, usuario):
    acervo.adicionar(obra)
    emprestimo = acervo.emprestar(obra, usuario)
    data_atrasada = emprestimo.previsao + timedelta(days=3)
    acervo.valor_multa(emprestimo, data_atrasada)
    assert usuario.divida == 3"""

from core import Acervo
from models import Obra, Usuario
from datetime import date, timedelta, datetime
from unittest.mock import patch
from database import criar_tabelas

def test_fluxo_emprestimo_com_mock():
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