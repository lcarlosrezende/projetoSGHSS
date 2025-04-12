from sqlalchemy import Column, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship

class Pessoa(Base):
    __tablename__ = "pessoa"

    pessoa_id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    contato = Column(String(20))
    email = Column(String(255), unique=True)
    senha_criptografada = Column(String(255), nullable=False)
    token_de_acesso = Column(String(255))
    funcao = Column(String(20), default="paciente") 
    paciente = relationship("Paciente", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")

