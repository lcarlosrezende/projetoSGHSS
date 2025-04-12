from sqlalchemy.orm import Session
from app.models.pessoa_model import Pessoa

def buscar_por_email(db: Session, email: str):
    return db.query(Pessoa).filter(Pessoa.email == email).first()

def criar_pessoa(db: Session, pessoa: Pessoa):
    db.add(pessoa)
    db.commit()
    db.refresh(pessoa)
    return pessoa
