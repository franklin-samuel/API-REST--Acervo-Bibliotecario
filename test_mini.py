import pytest
from datetime import date
from core import Acervo
from models import Usuario, Obra
from database import (
    salvar_usuario, buscar_obra_por_dados, limpar_tabelas,
    buscar_emprestimo, buscar_usuario
)


@pytest.fixture(autouse=True)
def setup_limpeza():
    limpar_tabelas()


def test_fluxo_completo_emprestimo_e_devolucao():
    acervo = Acervo()

    # Criar e salvar usuário
    usuario = Usuario(nome="Dezmetros", email="basquete@email.com")
    salvar_usuario(usuario)

    # Criar e adicionar obra (sincroniza ID internamente)
    obra = Obra(titulo="1984", autor="George Orwell", ano=1949, categoria="Ficção", quantidade=2)
    acervo.adicionar(obra)

    # Buscar novamente para garantir sincronização de ID
    obra_existente = buscar_obra_por_dados(obra.titulo, obra.autor, obra.ano, obra.categoria)
    assert obra_existente is not None
    obra.id = obra_existente.id
    
    # Realizar empréstimo
    emprestimo = acervo.emprestar(obra, usuario, dias=3)
    assert emprestimo.obra.id == obra.id
    assert emprestimo.usuario.id == usuario.id

    # Verificar se o empréstimo foi persistido corretamente
    emprestimo_db = buscar_emprestimo(str(emprestimo.id))
    assert emprestimo_db is not None
    assert emprestimo_db[1] == str(obra.id)
    assert emprestimo_db[2] == str(usuario.id)

    # Verificar estoque diminuiu
    obra_no_banco = acervo.encontrar_obra(obra.id)
    assert obra_no_banco.quantidade == 1

    # Devolver a obra
    acervo.devolver_por_id(str(emprestimo.id), data_devolucao=date.today())

    # Verificar se o estoque voltou ao normal
    obra_depois_devolucao = acervo.encontrar_obra(obra.id)
    assert obra_depois_devolucao.quantidade == 2

    # Verificar histórico do usuário (deve conter o título)
    tabela = acervo.historico_usuario(usuario)
    linhas = list(tabela.rows)
    assert len(linhas) == 1
    assert "1984" in linhas[0].cells[0]  # Título da obra

    # Verificar relatório de débitos (não deve haver dívida)
    relatorio = acervo.relatorio_debitos()
    assert len(list(relatorio.rows)) == 0
