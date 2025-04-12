from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Pessoa(Base):
    __tablename__ = 'pessoa'

    pessoa_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    contato = Column(String(20))
    email = Column(String(255))
    senha_criptografada = Column(String(255), nullable=False)
    token_de_acesso = Column(String(255))
