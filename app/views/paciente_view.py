from pydantic import BaseModel
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import verificar_token
from app.models.pessoa_model import Pessoa
from app.services import paciente_service
from app.schemas.paciente_schema import PacienteResponse, PacienteUpdate

router = APIRouter()

class PacienteResponse(BaseModel):
    paciente_id: int
    admissao_data: date
    diagnostico: str
    nome: str
    email: str

    class Config:
        orm_mode = True

@router.get("/{paciente_id}", response_model=PacienteResponse)
def buscar(paciente_id: int, db: Session = Depends(get_db), usuario: Pessoa = Depends(verificar_token)):
    paciente = paciente_service.buscar_paciente(db, paciente_id)
    
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    return {
        "paciente_id": paciente.paciente_id,
        "admissao_data": paciente.admissao_data,
        "diagnostico": paciente.diagnostico,
        "nome": paciente.pessoa.nome,
        "email": paciente.pessoa.email
    }

@router.get("/", response_model=list[PacienteResponse])
def listar_todos(db: Session = Depends(get_db), usuario: Pessoa = Depends(verificar_token)):
    pacientes = paciente_service.listar_pacientes(db)
    return [
        {
            "paciente_id": p.paciente_id,
            "admissao_data": p.admissao_data,
            "diagnostico": p.diagnostico,
            "nome": p.pessoa.nome,
            "email": p.pessoa.email
        } for p in pacientes
    ]

@router.put("/{paciente_id}", response_model=PacienteResponse)
def atualizar(paciente_id: int, dados: PacienteUpdate, db: Session = Depends(get_db), usuario: Pessoa = Depends(verificar_token)):
    paciente = paciente_service.atualizar_paciente(db, paciente_id, dados)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return {
        "paciente_id": paciente.paciente_id,
        "admissao_data": paciente.admissao_data,
        "diagnostico": paciente.diagnostico,
        "nome": paciente.pessoa.nome,
        "email": paciente.pessoa.email
    }

@router.delete("/{paciente_id}")
def excluir(paciente_id: int, db: Session = Depends(get_db), usuario: Pessoa = Depends(verificar_token)):
    paciente = paciente_service.excluir_paciente(db, paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return {"message": "Paciente excluído com sucesso"}
