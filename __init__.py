from models import Usuario, Obra
from core import Acervo
from datetime import date
import time

def executar_demo():
    acervo = Acervo()

    # criar usuario
    usuario = Usuario(nome="Dezmetros", email="basquete@email.com")
    obra = Obra(titulo="1984", autor="George Orwell", ano=1949, categoria="Ficção", quantidade=2)
    #adicionar no db
    salvar_usuario(usuario)
    acervo.adicionar(obra)
    
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
    devolvido = acervo.devolver_por_id(str(emprestimo.id), data_devolucao=date.today())
    print(f"\nDevolução registrada para o empréstimo ID {emprestimo.id} em {date.today()}")

    #relatorios
    print("\n=== Inventário Atual ===")
    print(acervo.relatorio_inventario())

    print("\n=== Relatório de Débitos ===")
    print(acervo.relatorio_debitos())

    print("\n=== Histórico do Usuário ===")
    print(acervo.historico_usuario(usuario))

if __name__ == "__main__":
    executar_demo()