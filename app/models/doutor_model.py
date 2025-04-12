# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from app.models.pessoa_model import Pessoa
# from app.core.database import Base

# class Doutor(Pessoa):
#     __tablename__ = 'doutor'
#     doutor_id = Column(Integer, ForeignKey('pessoa.pessoa_id'), primary_key=True)
#     nome = Column(String(20), nullable=False)
#     contato = Column(String(20), nullable=False)
#     email = Column(String(20), nullable=False)
#     agendamento = Column(String(20), nullable=False)
#     especializacao = Column(String(100), nullable=True)

#     doutor_id = Column(Integer, primary_key=True, index=True)
#     pessoa_id = Column(Integer, ForeignKey("pessoa.pessoa_id"))
#     pessoa = relationship("Pessoa", back_populates="doutor")


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.pessoa_model import Pessoa
from app.core.database import Base

class Doutor(Pessoa):
    __tablename__ = 'doutor'
    __mapper_args__ = {'polymorphic_identity': 'doutor'}

    doutor_id = Column(Integer, ForeignKey('pessoa.pessoa_id'), primary_key=True)
    agendamento = Column(String(20), nullable=False)
    especializacao = Column(String(100), nullable=True)

    # pessoa = relationship("Pessoa", back_populates="doutor")
    