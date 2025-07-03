from models import Usuario, Obra
from core import Acervo
from database import salvar_usuario, limpar_tabelas, buscar_obra_por_dados, listar_todas_obras, buscar_usuario_por_email
from datetime import date
from rich.console import Console
import time

def executar_demo():
    acervo = Acervo()

    # criar usuario
    usuario = buscar_usuario_por_email("basquete@email.com")
    if not usuario:
        usuario = Usuario(nome="Dezmetros", email="basquete@email.com")
        salvar_usuario(usuario)
        print(f"Usuário cadastrado: {usuario.nome} ({usuario.id})")
    else:
        print(f"Usuário já existente: {usuario.nome} ({usuario.id})")

    #buscar
    obra = Obra(titulo="1984", autor="George Orwell", ano=1949, categoria="Ficção", quantidade=1)
    acervo.adicionar(obra)

    # Recuperar do banco para garantir que o ID está sincronizado
    obra_existente = buscar_obra_por_dados(obra.titulo, obra.autor, obra.ano, obra.categoria)
    if obra_existente:
        obra.id = obra_existente.id
    
    print(f"Usuário cadastrado: {usuario.nome} ({usuario.id})")
    print(f"Obra cadastrada: {obra.titulo} ({obra.id})")

    #emprestar
    emprestimo = acervo.emprestar(obra, usuario, dias=3)
    print(f"\nObra emprestada: {emprestimo.obra.titulo} para {emprestimo.usuario.nome}")
    print(f"Previsão de devolução: {emprestimo.previsao}") 

    #buscar os dados
    usuario_encontrado = acervo.encontrar_usuario(str(usuario.id))
    obra_encontrada = acervo.encontrar_obra(str(obra.id))
    emprestimo_encontrado = acervo.encontrar_emprestimo(str(emprestimo.id))

    print("\n--- Dados recuperados do banco ---")
    print(f"Usuário: {usuario_encontrado.nome}")
    print(f"Obra: {obra_encontrada.titulo}")
    print(f"Empréstimo: {emprestimo_encontrado.obra.titulo} - Previsto para {emprestimo_encontrado.previsao}")

    #devolver
    acervo.devolver_por_id(str(emprestimo.id), data_devolucao=date.today())
    print(f"\nDevolução registrada para o empréstimo ID {emprestimo.id} em {date.today()}")

    #relatorios
    console = Console()
    print("\n=== Inventário Atual ===")
    console.print(acervo.relatorio_inventario())

    print("\n=== Relatório de Débitos ===")
    console.print(acervo.relatorio_debitos())

    print("\n=== Histórico do Usuário ===")
    console.print(acervo.historico_usuario(usuario))


executar_demo()
