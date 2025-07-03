from fastapi import FastAPI, HTTPException
from uuid import UUID
from core import Acervo
from models import Usuario, Obra
from datetime import date
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="API de Biblioteca",
    description="Gerencia obras, usuários e empréstimos de uma biblioteca escolar.",
    version="1.0.0"
)

acervo = Acervo()

# ------ Models Input ------

class ObraInput(BaseModel):
    """
    Modelo de entrada para cadastro de uma nova obra.
    """
    titulo: str
    autor: str
    ano: int
    categoria: str
    quantidade: int = 1

class UsuarioInput(BaseModel):
    """
    Modelo de entrada para cadastro de um novo usuário.
    """
    nome: str
    email: str

class EmprestimoInput(BaseModel):
    """
    Modelo de entrada para realizar um empréstimo.
    """
    id_usuario: UUID
    id_obra: UUID
    dias: int = 7

class DevolucaoInput(BaseModel):
    """
    Modelo de entrada para registrar devolução de um empréstimo.
    """
    emprestimo_id: UUID
    data_devolucao: Optional[date] = None

# ------ Rotas ------

@app.post("/obras/", summary="Cadastrar nova obra")
def criar_obra(obra: ObraInput):
    """
    Cadastra uma nova obra no acervo.

    - **titulo**: Título da obra
    - **autor**: Autor da obra
    - **ano**: Ano de publicação
    - **categoria**: Categoria (ex: Livro, Revista)
    - **quantidade**: Quantidade de exemplares disponíveis
    """
    nova_obra = Obra(
        titulo=obra.titulo,
        autor=obra.autor,
        ano=obra.ano,
        categoria=obra.categoria,
        quantidade=obra.quantidade
    )
    acervo.adicionar(nova_obra)
    return {"mensagem": "Obra adicionada com sucesso", "id": str(nova_obra.id)}

@app.post("/usuarios/", summary="Cadastrar novo usuário")
def criar_usuario(usuario: UsuarioInput):
    """
    Cadastra um novo usuário no sistema.

    - **nome**: Nome do usuário
    - **email**: Endereço de e-mail
    """
    novo_usuario = Usuario(usuario.nome, usuario.email)
    acervo.usuarios.add(novo_usuario)  # Certifique-se que `acervo.usuarios` existe e é um set

    return {
        "id": str(novo_usuario.id),
        "nome": novo_usuario.nome,
        "email": novo_usuario.email,
        "divida": novo_usuario.divida
    }

@app.post("/emprestar/", summary="Realizar empréstimo")
def emprestar_obra(dados: EmprestimoInput):
    """
    Realiza um empréstimo de uma obra para um usuário.

    - **id_usuario**: ID do usuário
    - **id_obra**: ID da obra
    - **dias**: Dias para devolução (padrão: 7)
    """
    try:
        emprestimo = acervo.emprestar_por_id(
            id_obra=dados.id_obra,
            id_usuario=dados.id_usuario,
            dias=dados.dias
        )
        return {
            "mensagem": "Empréstimo realizado com sucesso",
            "previsao_devolucao": str(emprestimo.previsao)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/devolver/", summary="Registrar devolução")
def devolver_obra(dados: DevolucaoInput):
    """
    Registra a devolução de uma obra emprestada.

    - **emprestimo_id**: ID do empréstimo
    - **data_devolucao**: Data da devolução (padrão: hoje)
    """
    emprestimo = acervo.devolver_por_id(dados.emprestimo_id, dados.data_devolucao)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    
    return {
        "mensagem": "Obra devolvida com sucesso!",
        "obra": emprestimo.obra.titulo,
        "usuario": emprestimo.usuario.nome,
        "data_devolucao": str(dados.data_devolucao or date.today())
    }

@app.get("/obras/", summary="Listar obras")
def listar_obras():
    """
    Lista todas as obras cadastradas no acervo.
    """
    return acervo.listar_obras()
