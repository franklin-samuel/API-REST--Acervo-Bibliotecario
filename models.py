import uuid
from datetime import datetime

class BaseEntity:
    """
    Classe base para entidades do sistema com ID único e data de criação.
    """

    def __init__(self):
        """
        Inicializa a entidade com um ID único e a data atual como data de criação.
        """
        self.id = self._gerar_id()
        self.data_criacao = datetime.now()

    def __eq__(self, other):
        """
        Compara duas entidades com base no ID.

        :param other: Outra instância para comparação.
        :return: True se os IDs forem iguais e o tipo for o mesmo.
        """
        return isinstance(other, self.__class__) and self.id == other.id
    
    def __hash__(self):
        """
        Retorna o hash da entidade com base no ID.

        :return: Hash do ID.
        """
        return hash(self.id)
    
    def _gerar_id(self):
        """
        Gera um UUID para identificar unicamente a entidade.

        :return: UUID gerado.
        """
        return uuid.uuid4()
    

class Obra(BaseEntity):
    """
    Representa uma obra (livro, revista, etc.) disponível para empréstimo.
    """

    def __init__(self, titulo, autor, ano, categoria, quantidade=1):
        """
        Inicializa uma obra com título, autor, ano, categoria e quantidade.

        :param titulo: Título da obra.
        :param autor: Autor da obra.
        :param ano: Ano de publicação.
        :param categoria: Categoria da obra.
        :param quantidade: Quantidade disponível (padrão: 1).
        """
        super().__init__()
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.categoria = categoria
        self.quantidade = quantidade
    
    def disponivel(self, estoque):
        """
        Verifica se a obra está disponível no estoque.

        :param estoque: Dicionário com IDs de obras e suas quantidades.
        :return: True se houver pelo menos uma unidade disponível.
        """
        return estoque.get(self.id, 0) > 0
    
    def __str__(self):
        """
        Retorna uma representação em string da obra.

        :return: String com título e ano.
        """
        return f"{self.titulo} ({self.ano})"


class Usuario(BaseEntity):
    """
    Representa um usuário do sistema de empréstimos.
    """

    def __init__(self, nome, email, divida=0):
        """
        Inicializa um usuário com nome, email e dívida (padrão: 0).

        :param nome: Nome do usuário.
        :param email: Email do usuário.
        :param divida: Valor da dívida atual do usuário.
        """
        super().__init__()
        self.nome = nome
        self.email = email
        self.divida = divida
    
    def __lt__(self, other):
        """
        Permite ordenação de usuários por nome.

        :param other: Outro usuário para comparação.
        :return: True se o nome for lexicograficamente menor.
        """
        return self.nome < other.nome
    
    def __str__(self):
        """
        Retorna o nome do usuário como string.

        :return: Nome do usuário.
        """
        return f"{self.nome}"


class Emprestimo(BaseEntity):
    """
    Representa um empréstimo de uma obra feito por um usuário.
    """

    def __init__(self, obra, usuario, data_emprestimo, data_prev_dev):
        """
        Inicializa um empréstimo com obra, usuário, data de empréstimo e data prevista de devolução.

        :param obra: Instância da obra emprestada.
        :param usuario: Instância do usuário que pegou emprestado.
        :param data_emprestimo: Data em que o empréstimo foi realizado.
        :param data_prev_dev: Data prevista para devolução.
        """
        super().__init__()
        self.obra = obra
        self.usuario = usuario
        self.data_emprestimo = data_emprestimo
        self.previsao = data_prev_dev

    def marcar_devolucao(self, data_devolucao):
        """
        Registra a data de devolução da obra.

        :param data_devolucao: Data em que a devolução foi realizada.
        """
        self.data_devolucao = data_devolucao
    
    def dias_atraso(self, data_ref):
        """
        Calcula o número de dias de atraso com base em uma data de referência.

        :param data_ref: Data utilizada para cálculo do atraso.
        :return: Número de dias em atraso (0 se dentro do prazo).
        """
        if data_ref > self.previsao:
            return (data_ref - self.previsao).days
        return 0
        
    def __str__(self):
        """
        Retorna uma representação simples do empréstimo com a data prevista de devolução.

        :return: String com a data prevista.
        """
        return f"prev: {self.previsao}"
