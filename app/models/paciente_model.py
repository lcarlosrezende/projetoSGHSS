from sqlalchemy import Column, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.pessoa_model import Pessoa

class Paciente(Base):
    __tablename__ = "paciente"

    paciente_id = Column(Integer, ForeignKey("pessoa.pessoa_id"), primary_key=True, index=True)
    admissao_data = Column(Date)
    diagnostico = Column(Text)

    pessoa = relationship("Pessoa", back_populates="paciente")
