from pydantic import BaseModel
from datetime import date
from typing import Optional

class PacienteBase(BaseModel):
    admissao_data: Optional[date] = None
    diagnostico: Optional[str] = None
    nome: Optional[str] = None  
    email: Optional[str] = None 

    class Config:
        orm_mode = True


class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(PacienteBase):
    pass

class PacienteResponse(PacienteBase):
    paciente_id: int
    nome: str  

    class Config:
        orm_mode = True
