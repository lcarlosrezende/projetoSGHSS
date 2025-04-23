from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.pessoa_model import Pessoa
from app.core.auth import criar_token
from app.services import pessoa_service
from app.core.database import get_db
from pydantic import BaseModel
from passlib.hash import bcrypt

router = APIRouter()

class LoginInput(BaseModel):
    email: str
    senha: str

@router.post("/register")
def registrar(nome: str, email: str, senha: str, contato: str, tipo: str, db: Session = Depends(get_db)):
    pessoa, erro = pessoa_service.registrar_usuario(db, nome, email, senha, contato, tipo)
    if erro:
        raise HTTPException(status_code=400, detail=erro)
    return {"message": "Usuário registrado com sucesso", "id": pessoa.pessoa_id}

@router.post("/login")
def login(dados: LoginInput, db: Session = Depends(get_db)):
    pessoa = db.query(Pessoa).filter(Pessoa.email == dados.email).first()
    if not pessoa or not bcrypt.verify(dados.senha, pessoa.senha_criptografada):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")
    
    token = criar_token(pessoa)
    return {"access_token": token, "token_type": "bearer"}
