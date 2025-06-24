from models import BaseEntity, Usuario, obra, Emprestimo
from datetime import datetime, timedelta
from database import salvar_emprestimo, registrar_devolucao
from rich.table import Table, Console

class Acervo:
    def __init__(self):
        self.acervo = {} #dicionario: {Obra: qtd_disponivel}
        self.usuarios = set() #lista de usuários com emprestimos
        self.historico_emprestimos = []
    
    def __iadd__(self, obra):
        if obra in self.acervo:
            self.acervo[obra] += 1
        else: 
            self.acervo[obra] = obra
        return self
    
    def __isub__(self, obra):
        if obra in self.acervo:
            if self.acervo[obra] > 1:
                self.acervo[obra] -= 1
            else:
                self.acervo.remove(obra)
        else: raise ValueError(f"A obra {obra} não está no acervo")
        return self
    
    def adicionar(self, obra): 
        self += obra

    def remover(self, obra):
        self -= obra

    def emprestar(self, obra, usuario, dias = 7):
        if obra not in self.acervo:
            raise ValueError(f"A obra {obra} não está disponível no acervo.")
        
        self -= obra
        data_emprestimo = datetime.now().date()
        data_prev_dev = data_emprestimo + timedelta(days=dias)
        emprestimo = Emprestimo(obra=obra, usuario=usuario, data_emprestimo=data_emprestimo, data_prev_dev=data_prev_dev)

        self.usuarios.add(usuario)
        self.historico_emprestimos.append(emprestimo)
        salvar_emprestimo(emprestimo)
        return emprestimo
    
    def devolver(self, emprestimo, data_dev):
        emprestimo.marcar_devolucao(data_dev)
        registrar_devolucao(emprestimo.id, data_dev)
        self += emprestimo.obra

    def valor_multa(self, emprestimo, data_ref):
        dias_atrasados = emprestimo.dias_atraso(data_ref)
        multa_por_dia = 1
        valor_total = dias_atrasados * multa_por_dia

        if valor_total > 0:
            emprestimo.usuario.divida += valor_total

    def relatorio_inventario(self):
        table = Table(title="Todos os Livros", show_lines=True)

        for col in ("id", "Título", "Autor", "Ano", "Categoria", "Quantidade"):
            table.add_column(col, style="cyan", justify="center")

        for obra in self.acervo.items():
            table.add_row(
                str(obra.id),
                obra.titulo,
                obra.autor,
                str(obra.ano),
                obra.categoria,
                str(obra.quantidade)
            )

        return table
    
    def relatorio_debitos(self):
        table = Table(title='Débitos de usuários', show_lines=True)

        for col in ("id", "Nome", "Email", "Dívida"):
            table.add_column(col, style="cyan", justify="center")

        for usuario in self.usuarios:
            if usuario.divida > 0:
                table.add_row(
                    usuario.id,
                    usuario.nome,
                    usuario.email,
                    f"{usuario.divida:.2f}"
                )

        return table
    
    def historico_usuario(self, usuario):
        table = Table(title=f"Histórico de Empréstimos - {usuario.nome}")

        for col in ("Título da Obra", "Empréstimo", "Previsão", "Devolução", "Status"):
            table.add_column(col, style="cyan", justify="center")

        for emprestimo in self.historico_emprestimos:
            if emprestimo.usuario == usuario:
                data_dev = getattr(emprestimo, "data_devolucao", None)
                status = "Devolvido" if data_dev else "Em andamento"
                table.add_row(
                    emprestimo.obra.titulo,
                    str(emprestimo.data_emprestimo),
                    str(emprestimo.previsao),
                    str(data_dev) if data_dev else "-",
                    status
                )

        return table


        
    
