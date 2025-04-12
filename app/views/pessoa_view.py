from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services import pessoa_service
from app.core.database import get_db

router = APIRouter()

@router.post("/register")
def registrar(nome: str, email: str, senha: str, contato: str, db: Session = Depends(get_db)):
    pessoa, erro = pessoa_service.registrar_usuario(db, nome, email, senha, contato)
    if erro:
        raise HTTPException(status_code=400, detail=erro)
    return {"message": "Usuário registrado com sucesso", "id": pessoa.pessoa_id}

@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    token = pessoa_service.autenticar_usuario(db, email, senha)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")
    return {"access_token": token, "token_type": "bearer"}
