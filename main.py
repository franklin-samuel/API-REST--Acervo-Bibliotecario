from fastapi import FastAPI
from uuid import UUID
from core import Acervo
from models import Usuario, Obra
from datetime import date, datetime, timedelta
from pydantic import BaseModel

app = FastAPI()
acervo = Acervo()

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

