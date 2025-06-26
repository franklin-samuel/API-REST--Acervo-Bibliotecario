<<<<<<< Updated upstream
"""import pytest
from datetime import datetime, timedelta
from models import Usuario, Obra, Emprestimo
=======
>>>>>>> Stashed changes
from core import Acervo
from models import Obra, Usuario
from datetime import date, timedelta
from unittest.mock import patch

with patch("database.salvar_obra") as mock_salvar_obra, \
     patch("database.salvar_usuario") as mock_salvar_usuario, \
     patch("database.salvar_emprestimo") as mock_salvar_emprestimo:

    acervo = Acervo()

    livro = Obra("POO Essencial", "Ana Silva", 2025, "Livro", 2)
    joao  = Usuario("João", "joao@example.com")

    # Chama as funções de salvar (mockadas)
    mock_salvar_obra(livro)
    mock_salvar_usuario(joao)

    acervo += livro

    emp = acervo.emprestar(livro, joao)

    mock_salvar_emprestimo(emp)

    after3 = date.today() + timedelta(days=3)
    print("Multa:", acervo.valor_multa(emp, after3))

<<<<<<< Updated upstream
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
from database import criar_tabelas, limpar_tabelas

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
=======
    print(acervo.relatorio_inventario())

    # Opcional: você pode checar quantas vezes foram chamadas
    print("salvar_obra chamada:", mock_salvar_obra.call_count)
    print("salvar_usuario chamada:", mock_salvar_usuario.call_count)
    print("salvar_emprestimo chamada:", mock_salvar_emprestimo.call_count)
>>>>>>> Stashed changes
