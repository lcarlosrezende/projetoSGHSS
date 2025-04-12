from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import relationship

class DoutorBase(BaseModel):
    nome: str
    contato: str
    email: str
    senha: str  
    especializacao: Optional[str] 

class DoutorCreate(DoutorBase):
    pass

class DoutorResponse(BaseModel):
    doutor_id: int
    nome: str
    email: str
    contato: str
    especializacao: Optional[str]  

    class Config:
        orm_mode = True
