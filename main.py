from fastapi import FastAPI, HTTPException
from uuid import UUID
from core import Acervo
from models import Usuario, Obra
from datetime import date, datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()
acervo = Acervo()

#------Models Input------
class ObraInput(BaseModel):
    titulo: str
    autor: str
    ano: int
    categoria: str
    quantidade: int = 1

class UsuarioInput(BaseModel):
    nome: str
    email: str

class EmprestimoInput(BaseModel):
    id_usuario: UUID
    id_obra: UUID
    dias: int = 7

class DevolucaoInput(BaseModel):
    emprestimo_id: UUID
    data_devolucao: Optional[date] = None

@app.post("/obras/")
def criar_obra(obra: ObraInput):
    nova_obra = Obra(titulo = obra.titulo, autor = obra.autor, ano = obra.ano, categoria = obra.categoria, quantidade = obra.quantidade)
    acervo.adicionar(nova_obra)

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


@app.post("/emprestar/")
def emprestar_obra(dados: EmprestimoInput):
    try:
        emprestimo = acervo.emprestar_por_id(id_obra=dados.id_obra, id_usuario=dados.id_usuario, dias=dados.dias)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/devolver/")
def devolver_obra(dados: DevolucaoInput):
    emprestimo = acervo.devolver_por_id(dados.emprestimo_id, dados.data_devolucao)
    if not emprestimo:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")
    
    return {
        "mensagem": "Obra devolvida com sucesso!",
        "obra": emprestimo.obra.titulo,
        "usuario": emprestimo.usuario.nome,
        "data_devolucao": str(dados.data_devolucao or date.today())
    }

@app.get("/obras/")
def listar_obras():
    return acervo.listar_obras()
