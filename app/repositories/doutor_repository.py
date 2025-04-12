from sqlalchemy.orm import Session
from app.models.doutor_model import Doutor

def listar_doutores(db: Session):
    return db.query(Doutor).all()

def buscar_doutor_por_id(db: Session, doutor_id: int):
    return db.query(Doutor).filter(Doutor.doutor_id == doutor_id).first()

def criar_doutor(db: Session, doutor: Doutor):
    db.add(doutor)
    db.commit()
    db.refresh(doutor)
    return doutor

def remover_doutor(db: Session, doutor: Doutor):
    db.delete(doutor)
    db.commit()
