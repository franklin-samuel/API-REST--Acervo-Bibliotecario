from models import BaseEntity, Usuario, Obra, Emprestimo
from datetime import datetime, timedelta, date
from database import salvar_emprestimo, registrar_devolucao, salvar_usuario, salvar_obra
from rich.table import Table


class Acervo:
    def __init__(self):
        self.acervo = {}  # dicionário: {Obra: qtd_disponivel}
        self.usuarios = set() # set: lista de usuários
        self.historico_emprestimos = [] # lista de emprestimos de um usuário

    def __iadd__(self, obra):
        if obra in self.acervo:
            self.acervo[obra] += 1
        else:
            self.acervo[obra] = 1
        return self

    def __isub__(self, obra):
        if obra in self.acervo:
            if self.acervo[obra] > 1:
                self.acervo[obra] -= 1
            else:
                del self.acervo[obra]
        else:
            raise ValueError(f"A obra {obra} não está no acervo")
        return self
    
    #add/remove
    def adicionar(self, obra):
        self.__valida_obra(obra)
        self += obra
        salvar_obra(obra)

    def remover(self, obra):
        self.__valida_obra(obra)
        self -= obra

    #Busca
    def encontrar_usuario(self, id_usuario):
        return next((u for u in self.usuarios if u.id == id_usuario), None)

    def encontrar_obra(self, id_obra):
        return next((o for o in self.acervo if o.id == id_obra), None)
    
    #Emprestar
    def emprestar(self, obra, usuario, dias=7):
        self.__valida_obra(obra)

        if obra not in self.acervo:
            raise ValueError(f"A obra {obra} não está disponível no acervo.")

        self -= obra
        data_emprestimo = datetime.now().date()
        data_prev_dev = data_emprestimo + timedelta(days=dias)
        emprestimo = Emprestimo(
            obra=obra,
            usuario=usuario,
            data_emprestimo=data_emprestimo,
            data_prev_dev=data_prev_dev
        )

        self.usuarios.add(usuario)
        self.historico_emprestimos.append(emprestimo)
        salvar_emprestimo(emprestimo)
        return emprestimo
    
    def emprestar_por_id(self, id_obra, id_usuario, dias=7):
        obra = self.encontrar_obra(id_obra)
        usuario = self.encontrar_usuario(id_usuario)

        if not obra or not usuario:
            raise ValueError("Obra ou usuários não encontrados.")
        
        return self.emprestar(obra, usuario, dias)

    #Devolver
    def devolver(self, emprestimo, data_dev):
        emprestimo.marcar_devolucao(data_dev)
        registrar_devolucao(emprestimo.id, data_dev)
        self += emprestimo.obra
    
    def devolver_por_id(self, id_emprestimo, data_devolucao=None):
        emprestimo = next((e for e in self.historico_emprestimos if e.id == id_emprestimo), None)

        if not emprestimo:
            return None
        
        self.devolver(emprestimo, data_devolucao or date.today())
        return emprestimo

    #Multa
    def valor_multa(self, emprestimo, data_ref):
        dias_atrasados = emprestimo.dias_atraso(data_ref)
        multa_por_dia = 1
        valor_total = dias_atrasados * multa_por_dia

        if valor_total > 0:
            emprestimo.usuario.divida += valor_total
            salvar_usuario(emprestimo.usuario)
        
        return float(valor_total)
    
    #Listar Obras
    def listar_obras(self):
        obras = []
        for obra, quantidade in self.acervo.items():
            obras.append({
                "id": str(obra.id),
                "titulo": obra.titulo,
                "autor": obra.autor,
                "ano": obra.ano,
                "categoria": obra.categoria,
                "quantidade": quantidade
            })

        return obras

    def relatorio_inventario(self):
        builder = self._relatorio_builder("Todos os Livros")
        builder.add_colunas(
            ("ID", "cyan", "center"),
            ("Título", "magenta", "center"),
            ("Autor", "green", "center"),
            ("Ano", "blue", "center"),
            ("Categoria", "white", "center"),
            ("Quantidade", "bold yellow", "center")
        )

        for obra, quantidade in self.acervo.items():
            builder.add_linha(
                str(obra.id),
                obra.titulo,
                obra.autor,
                str(obra.ano),
                obra.categoria,
                str(quantidade)
            )

        return builder.build()

    def relatorio_debitos(self):
        builder = self._relatorio_builder("Débitos de Usuários")
        builder.add_colunas(
            ("ID", "cyan", "center"),
            ("Nome", "magenta", "center"),
            ("Email", "green", "center"),
            ("Dívida (R$)", "bold red", "center")
        )

        for usuario in self.usuarios:
            if usuario.divida > 0:
                builder.add_linha(
                    str(usuario.id),
                    usuario.nome,
                    usuario.email,
                    f"{usuario.divida:.2f}"
                )

        return builder.build()

    def historico_usuario(self, usuario):
        builder = self._relatorio_builder(f"Histórico de Empréstimos - {usuario.nome}")
        builder.add_colunas(
            ("Título da Obra", "magenta", "center"),
            ("Empréstimo", "cyan", "center"),
            ("Previsão", "cyan", "center"),
            ("Devolução", "yellow", "center"),
            ("Status", "green", "center")
        )

        for emprestimo in self.historico_emprestimos:
            if emprestimo.usuario == usuario:
                data_dev = getattr(emprestimo, "data_devolucao", None)
                status = "Devolvido" if data_dev else "Em andamento"
                builder.add_linha(
                    emprestimo.obra.titulo,
                    str(emprestimo.data_emprestimo),
                    str(emprestimo.previsao),
                    str(data_dev) if data_dev else "-",
                    status
                )

        return builder.build()

    def __valida_obra(self, obra):
        from models import Obra as ObraClass
        if not isinstance(obra, ObraClass):
            raise TypeError(f'Esperado tipo obra, mas recebeu {type(obra).__name__}.')

    def _relatorio_builder(self, titulo):
        return self._RelatorioBuilder(titulo)

    class _RelatorioBuilder:
        def __init__(self, titulo):
            self.tabela = Table(title=titulo, show_lines=True)

        def add_colunas(self, *colunas):
            for nome, estilo, alinhamento in colunas:
                self.tabela.add_column(nome, style=estilo, justify=alinhamento)

        def add_linha(self, *valores):
            self.tabela.add_row(*[str(v) for v in valores])

        def build(self):
            return self.tabela
