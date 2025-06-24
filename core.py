from models import BaseEntity, Usuario, obra, Emprestimo

class Acervo:
    def __init__(self):
        self.acervo = {} #dicionario: {Obra: qtd_disponivel}
    
    def __iadd__(self, obra):
        if obra in self.acervo:
            self.acervo[obra] += 1
        else: 
            self.acervo[obra] = obra
        return Acervo

    def __isub__(self, obra):
        if obra in self.acervo:
            if self.acervo[obra] > 1:
                self.acervo[obra] -= 1
            else:
                self.acervo.remove(obra)
        return Acervo