from models import BaseEntity, Usuario, obra, Emprestimo
from datetime import datetime, timedelta
from rich.table import Table, Console

class Acervo:
    def __init__(self):
        self.acervo = {} #dicionario: {Obra: qtd_disponivel}
    
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
        return emprestimo
    
    def devolver(self, emprestimo, data_dev):
        emprestimo.marcar_devolucao(data_dev)
        self += emprestimo.obra

    def valor_multa(self, emprestimo, data_ref):
        dias_atrasados = emprestimo.dias_atraso(data_ref)
        multa_por_dia = 1
        valor_total = dias_atrasados * multa_por_dia

        if valor_total > 0:
            emprestimo.usuario.divida += valor_total

    def relatorio_inventario(self):

        console = Console()

        table = Table(title="Todos os Livros", show_lines=True)
        for col in ("id", "Título", "Autor", "Ano", "Categoria", "Quantidade"):
            table.add_column(col, style="cyan", justify="center")
        for obra, quantidade in self.acervo.items():
            table.add_row(
                str(obra.id),
                obra.titulo,
                obra.autor,
                str(obra.ano),
                obra.categoria,
                str(obra.quantidade)
            )

        return table
        
    
