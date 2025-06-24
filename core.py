from models import BaseEntity, Usuario, obra, Emprestimo
from datetime import datetime, timedelta
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
        emprestimo.dias_atraso(data_ref)
        