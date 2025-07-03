from models import BaseEntity, Usuario, Obra, Emprestimo
from datetime import datetime, timedelta, date
from database import (
    salvar_emprestimo, registrar_devolucao, salvar_usuario, salvar_obra,
    atualizar_quantidade_obra, buscar_obra, buscar_usuario, listar_todas_obras,
    buscar_emprestimo, listar_usuarios_com_divida, buscar_emprestimos_por_usuario
)
from rich import Table
import uuid


class Acervo:
    """
    Representa o acervo de obras e gerenciamento de empréstimos de uma biblioteca.
    Fornece funcionalidades para adicionar/remover obras, emprestar, devolver e gerar relatórios.
    """

    def __init__(self):
        """Inicializa uma instância do acervo."""
        pass

    def __iadd__(self, obra):
        """
        Adiciona uma obra ao acervo (opera o +=).
        Salva a obra no banco de dados.

        :param obra: Instância de Obra.
        :return: A instância atual do acervo.
        """
        self.__valida_obra(obra)
        salvar_obra(obra)
        return self

    def __isub__(self, obra):
        """
        Remove uma unidade da obra do acervo (opera o -=).
        Atualiza a quantidade no banco de dados.

        :param obra: Instância de Obra.
        :return: A instância atual do acervo.
        """
        self.__valida_obra(obra)
        atualizar_quantidade_obra(obra.id, -1)
        return self
    
    # Adicionar/Remover
    def adicionar(self, obra):
        """Interface pública para adicionar uma obra ao acervo."""
        self.__valida_obra(obra)
        self += obra

    def remover(self, obra):
        """Interface pública para remover uma obra do acervo."""
        self.__valida_obra(obra)
        self -= obra

    # Busca
    def encontrar_usuario(self, id_usuario):
        """
        Busca um usuário no banco pelo ID.

        :param id_usuario: UUID do usuário.
        :return: Instância de Usuario ou None.
        """
        row = buscar_usuario(id_usuario)
        if row:
            usuario = Usuario(row[1], row[2], row[3])
            usuario.id = uuid.UUID(row[0])
            return usuario
        return None
        
    def encontrar_obra(self, id_obra):
        """
        Busca uma obra no banco pelo ID.

        :param id_obra: UUID da obra.
        :return: Instância de Obra ou None.
        """
        row = buscar_obra(id_obra)
        if row:
            obra = Obra(row[1], row[2], row[3], row[4], row[5])
            obra.id = uuid.UUID(row[0])
            return obra
        return None
    
    def encontrar_emprestimo(self, id_emprestimo):
        """
        Busca um empréstimo no banco pelo ID.

        :param id_emprestimo: UUID do empréstimo.
        :return: Instância de Emprestimo ou None.
        """
        row = buscar_emprestimo(id_emprestimo)
        if row:
            emprestimo = Emprestimo(row[1], row[2], row[3], row[4])
            emprestimo.id = uuid.UUID(row[0])
            return emprestimo
        return None

    # Empréstimo
    def emprestar(self, obra, usuario, dias=7):
        """
        Realiza o empréstimo de uma obra para um usuário, se houver unidades disponíveis.

        :param obra: Instância da Obra.
        :param usuario: Instância do Usuario.
        :param dias: Número de dias até a devolução.
        :return: Instância de Emprestimo.
        """
        self.__valida_obra(obra)

        row = buscar_obra(obra.id)
        if not row or row[5] <= 0:
            raise ValueError("Obra não tem estoque disponível, tente outra.")

        atualizar_quantidade_obra(obra.id, -1)

        data_emprestimo = datetime.now().date()
        data_prev_dev = data_emprestimo + timedelta(days=dias)
        emprestimo = Emprestimo(
            obra=obra,
            usuario=usuario,
            data_emprestimo=data_emprestimo,
            data_prev_dev=data_prev_dev
        )

        salvar_emprestimo(emprestimo)
        return emprestimo
    
    def emprestar_por_id(self, id_obra, id_usuario, dias=7):
        """
        Realiza o empréstimo com base nos IDs de obra e usuário.

        :param id_obra: UUID da obra.
        :param id_usuario: UUID do usuário.
        :param dias: Número de dias até devolução.
        :return: Instância de Emprestimo.
        """
        obra = self.encontrar_obra(id_obra)
        usuario = self.encontrar_usuario(id_usuario)

        if not obra or not usuario:
            raise ValueError("Obra ou usuário não encontrados.")
        
        return self.emprestar(obra, usuario, dias)

    # Devolução
    def devolver(self, emprestimo, data_dev):
        """
        Realiza a devolução de um empréstimo.

        :param emprestimo: Instância de Emprestimo.
        :param data_dev: Data da devolução.
        """
        emprestimo.marcar_devolucao(data_dev)
        registrar_devolucao(emprestimo.id, data_dev)
        self += emprestimo.obra
    
    def devolver_por_id(self, id_emprestimo, data_devolucao=None):
        """
        Devolve um empréstimo com base no ID.

        :param id_emprestimo: UUID do empréstimo.
        :param data_devolucao: Data da devolução, ou data atual por padrão.
        :return: Emprestimo atualizado ou None.
        """
        emprestimo = self.encontrar_emprestimo(id_emprestimo)

        if not emprestimo:
            return None
        
        self.devolver(emprestimo, data_devolucao or date.today())
        return emprestimo

    # Multa
    def valor_multa(self, emprestimo, data_ref):
        """
        Calcula o valor da multa por atraso e atualiza a dívida do usuário.

        :param emprestimo: Instância de Emprestimo.
        :param data_ref: Data de referência (ex: hoje).
        :return: Valor da multa em float.
        """
        dias_atrasados = emprestimo.dias_atraso(data_ref)
        multa_por_dia = 1
        valor_total = dias_atrasados * multa_por_dia

        if valor_total > 0:
            emprestimo.usuario.divida += valor_total
            salvar_usuario(emprestimo.usuario)
        
        return float(valor_total)
    
    # Listagem
    def listar_obras(self):
        """
        Lista todas as obras do acervo.

        :return: Lista de dicionários com dados das obras.
        """
        rows = listar_todas_obras()
        obras = []
        for row in rows:
            obras.append({
                "id": row[0],
                "titulo": row[1],
                "autor": row[2],
                "ano": row[3],
                "categoria": row[4],
                "quantidade": row[5]
            })
        return obras

    # Relatórios
    def relatorio_inventario(self):
        """
        Gera um relatório Rich com todas as obras do acervo.

        :return: Instância de rich.Table.
        """
        builder = self._relatorio_builder("Todos os Livros")
        builder.add_colunas(
            ("ID", "cyan", "center"),
            ("Título", "magenta", "center"),
            ("Autor", "green", "center"),
            ("Ano", "blue", "center"),
            ("Categoria", "white", "center"),
            ("Quantidade", "bold yellow", "center")
        )

        rows = listar_todas_obras()
        for row in rows:
            builder.add_linha(
                row[0],  
                row[1],  
                row[2],  
                str(row[3]), 
                row[4], 
                str(row[5])   
            )
        return builder.build()

    def relatorio_debitos(self):
        """
        Gera um relatório com os usuários que possuem dívidas.

        :return: Instância de rich.Table.
        """
        builder = self._relatorio_builder("Débitos de Usuários")
        builder.add_colunas(
            ("ID", "cyan", "center"),
            ("Nome", "magenta", "center"),
            ("Email", "green", "center"),
            ("Dívida (R$)", "bold red", "center")
        )

        rows = listar_usuarios_com_divida()
        for row in rows:
            builder.add_linha(
                row[0],
                row[1],
                row[2],
                row[3]
            )

        return builder.build()

    def historico_usuario(self, usuario):
        """
        Gera um relatório com o histórico de empréstimos de um usuário.

        :param usuario: Instância de Usuario.
        :return: Instância de rich.Table.
        """
        builder = self._relatorio_builder(f"Histórico de Empréstimos - {usuario.nome}")
        builder.add_colunas(
            ("Título da Obra", "magenta", "center"),
            ("Empréstimo", "cyan", "center"),
            ("Previsão", "cyan", "center"),
            ("Devolução", "yellow", "center"),
            ("Status", "green", "center")
        )

        emprestimos = buscar_emprestimos_por_usuario(usuario.id)  
        for row in emprestimos:
            titulo_obra = row[5]
            data_emp = row[2]
            previsao = row[3]
            data_dev = row[4]
            status = "Devolvido" if data_dev else "Em andamento"

            builder.add_linha(
                titulo_obra,
                str(data_emp),
                str(previsao),
                str(data_dev) if data_dev else "-",
                status
            )

        return builder.build()

    def __valida_obra(self, obra):
        """
        Valida se o objeto fornecido é uma instância de Obra.

        :param obra: Objeto a ser validado.
        :raises TypeError: Se o objeto não for uma Obra.
        """
        from models import Obra as ObraClass
        if not isinstance(obra, ObraClass):
            raise TypeError(f'Esperado tipo obra, mas recebeu {type(obra).__name__}.')

    def _relatorio_builder(self, titulo):
        """
        Cria e retorna um construtor de relatório.

        :param titulo: Título do relatório.
        :return: Instância de _RelatorioBuilder.
        """
        return self._RelatorioBuilder(titulo)

    class _RelatorioBuilder:
        """
        Classe auxiliar interna para construir tabelas Rich formatadas.
        """

        def __init__(self, titulo):
            self.tabela = Table(title=titulo, show_lines=True)

        def add_colunas(self, *colunas):
            """
            Adiciona colunas à tabela.

            :param colunas: Tuplas (nome, estilo, alinhamento).
            """
            for nome, estilo, alinhamento in colunas:
                self.tabela.add_column(nome, style=estilo, justify=alinhamento)

        def add_linha(self, *valores):
            """
            Adiciona uma linha à tabela.

            :param valores: Valores a serem convertidos para string e exibidos.
            """
            self.tabela.add_row(*[str(v) for v in valores])

        def build(self):
            """
            Constrói e retorna a tabela Rich.

            :return: Instância de rich.Table.
            """
            return self.tabela
