from models import Usuario, Obra
from acervo import Acervo
from datetime import date

def executar_demo():
    acervo = Acervo()

    #criar usuario
    usuario = Usuario(nome="Dezmetros", email="lebron@email.com")
    print(f"Usuário criado: {usuario.nome} - {usuario.email}")

    #criar obra
    obra = Obra(titulo="1984", autor="George Orwell", ano=1949, categoria="Ficção", quantidade=2)
    print(f"Obra criada: {obra.titulo} - {obra.autor}")
    
    #adicionar
    acervo.adicionar(obra)
    salvar_usuario(usuario)
    
    #fazer emprestimo
    emprestimo = acervo.emprestar(obra, usuario, dias=5)
    print(f"Emprestado: {emprestimo.obra.titulo} para {emprestimo.usuario.nome} até {emprestimo.previsao}")
    
    #relatorio do inventario
    print("\n -Inventário Atual ")
    print(acervo.relatorio_inventario())
    
    #historico do usuario
    print("\n -Histórico do Usuario")
    print(acervo.historico_usuario(usuario))

if __name__ == "__main__":
    executar_demo()