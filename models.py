import uuid
from datetime import datetime

class BaseEntity:
    def __init__(self):
        self.id = self._gerar_id()
        self.data_criacao = datetime.now()

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.id == other.id
    
    def __hash__(self):
        return hash(self.id)
    
    def _gerar_id(self):
        return uuid.uuid4()
    

class Obra(BaseEntity):
    def __init__(self, titulo, autor, ano, categoria, quantidade=1):
        super().__init__()
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.categoria = categoria
        self.quantidade = quantidade
    
    def disponivel(self, estoque):
        return estoque.get(self.id, 0) > 0
    
    def __str__(self):
        return f"{self.titulo} ({self.ano})"

class Usuario(BaseEntity):
    def __init__(self, nome, email):
        super().__init__()
        self.nome = nome
        self.email = email
        self.divida = 0
    
    def __lt__(self, other):
        return self.nome < other.nome
    
    def __str__(self):
        return f"{self.nome}"


class Emprestimo(BaseEntity):
    def __init__(self, obra, usuario, data_emprestimo, data_prev_dev):
        super().__init__()
        self.obra = obra
        self.usuario = usuario
        self.data_emprestimo = data_emprestimo
        self.previsao = data_prev_dev

    def marcar_devolucao(self, data_devolucao):
        self.data_devolucao = data_devolucao
    
    def dias_atraso(self, data_ref):
        if data_ref > (self.previsao):
            return (data_ref - self.previsao).days
        return 0
        
    def __str__(self):
        return f"prev: {self.previsao}"

