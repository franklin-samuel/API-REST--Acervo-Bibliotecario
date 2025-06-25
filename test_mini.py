import pytest
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
    assert usuario.divida == 3