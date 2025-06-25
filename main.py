from fastapi import FastAPI
from uuid import UUID
from core import Acervo
from models import Usuario, Obra
from datetime import date, datetime, timedelta
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
acervo = Acervo()

class ObraInput(BaseModel):
    titulo: str
    autor: str
    ano: int
    categoria: str
    quantidade: int = 1

@app.post("/obras/")
def criar_obra(obra: ObraInput):
    nova_obra = Obra(titulo = obra.titulo, autor = obra.autor, ano = obra.ano, categoria = obra.categoria, quantidade = obra.quantidade)

    acervo.adicionar(nova_obra)


class UsuarioInput(BaseModel):
    nome: str
    email: str

@app.post("/usuarios/")
def criar_usuario(usuario: UsuarioInput):
    novo_usuario = Usuario(usuario.nome, usuario.email)
    acervo.usuarios.add(novo_usuario)
    
    return {
        "id": str(novo_usuario.id),
        "nome": novo_usuario.nome,
        "email": novo_usuario.email,
        "divida": novo_usuario.divida
    }

class EmprestimoInput(BaseModel):
    id_usuario: UUID
    id_obra: UUID
    dias: int = 7

@app.post("/emprestar/")
def emprestar_obra(dados: EmprestimoInput):
    usuario = next((user for user in acervo.usuarios if user.id == dados.id_usuario), None)
    if not usuario:
        return {"erro": "Usuário não encontrado"}
    

    obra = next((ob for ob in acervo.acervo if ob.id == dados.id_obra), None)
    if not obra:
        return {"erro": "Obra não encontrada"}
    
    try:
        emprestimo = acervo.emprestar(obra, usuario, dias=dados.dias)
    except ValueError as e:
        return {"erro": str(e)
     
    }

    return {
        "emprestimo_id": str(emprestimo.id),
        "usuario": usuario.nome,
        "data_emprestimo": str(emprestimo.data_emprestimo),
        "previsao_devolucao": str(emprestimo.previsao)
    }

class DevolucaoInput(BaseModel):
    emprestimo_id: UUID
    data_devolucao: Optional[date] = None

@app.post("/devolver/")
def devolver_obra(dados: DevolucaoInput):
    emprestimo = next((emp for emp in acervo.historico_emprestimos if emp.id == dados.emprestimo_id), None)

    if not emprestimo:
        return {"erro": "Empréstimo não encontrado"}
    
    data_dev = dados.data_devolucao or date.today()

    acervo.devolver(emprestimo, data_dev)

    return {
        "mensagem": "Obra devolvida com sucesso!",
        "obra": emprestimo.obra.titulo,
        "usuario": emprestimo.usuario.nome,
        "data_devolucao": str(data_dev)
    }

