from sqlalchemy.orm import Session
from app.models.paciente_model import Paciente
from app.schemas.paciente_schema import PacienteCreate, PacienteUpdate
from datetime import date

def buscar_paciente(db: Session, paciente_id: int) -> Paciente:
    return db.query(Paciente).filter(Paciente.paciente_id == paciente_id).first()

def listar_pacientes(db: Session):
    return db.query(Paciente).all()

def atualizar_paciente(db: Session, paciente_id: int, dados: PacienteUpdate):
    paciente = db.query(Paciente).filter(Paciente.paciente_id == paciente_id).first()

    if not paciente:
        return None

    if dados.admissao_data is not None:
        paciente.admissao_data = dados.admissao_data
    if dados.diagnostico is not None:
        paciente.diagnostico = dados.diagnostico
    if dados.nome is not None:
        paciente.pessoa.nome = dados.nome 
    if dados.nome is not None:
        paciente.pessoa.email = dados.email 

    db.commit()
    db.refresh(paciente)
    return paciente


from fastapi import HTTPException, status

def excluir_paciente(db: Session, paciente_id: int):
    paciente = db.query(Paciente).filter(Paciente.paciente_id == paciente_id).first()

    if not paciente:
        # Retornar erro 404 caso o paciente não seja encontrado
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado.")

    # Excluir o paciente (isso vai excluir a pessoa em cascata)
    db.delete(paciente)
    db.commit()

    # Retornar o paciente excluído como confirmação
    return paciente

