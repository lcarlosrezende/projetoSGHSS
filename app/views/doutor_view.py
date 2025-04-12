from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.doutor_schema import DoutorCreate, DoutorResponse
from app.services import doutor_service
from app.core.database import Base
from app.core.auth import verificar_token
from app.core.database import get_db

router = APIRouter(prefix="/api/doutores", tags=["Doutores"])

@router.get("/", response_model=List[DoutorResponse], dependencies=[Depends(verificar_token)])
def listar_doutores(db: Session = Depends(get_db)):
    return doutor_service.listar_doutores(db)

@router.get("/{doutor_id}", response_model=DoutorResponse, dependencies=[Depends(verificar_token)])
def buscar_doutor(doutor_id: int, db: Session = Depends(get_db)):
    doutor = doutor_service.buscar_doutor(db, doutor_id)
    if not doutor:
        raise HTTPException(status_code=404, detail="Doutor não encontrado")
    return doutor

@router.post("/", response_model=DoutorResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(verificar_token)])
def criar_doutor(doutor: DoutorCreate, db: Session = Depends(get_db)):
    return doutor_service.criar_doutor(db, doutor)

@router.delete("/{doutor_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(verificar_token)])
def excluir_doutor(doutor_id: int, db: Session = Depends(get_db)):
    if not doutor_service.excluir_doutor(db, doutor_id):
        raise HTTPException(status_code=404, detail="Doutor não encontrado")
