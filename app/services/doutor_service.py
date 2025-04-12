from sqlalchemy.orm import Session
from app.models.doutor_model import Doutor
from app.schemas.doutor_schema import DoutorCreate
from app.core.auth import gerar_hash
from app.repositories import doutor_repository
from passlib.context import CryptContext
from app.models.pessoa_model import Pessoa
from app.models.doutor_model import Doutor
from fastapi import HTTPException
from passlib.context import CryptContext

def listar_doutores(db: Session):
    return doutor_repository.listar_doutores(db)

def buscar_doutor(db: Session, doutor_id: int):
    return doutor_repository.buscar_doutor_por_id(db, doutor_id)

from fastapi import HTTPException

from fastapi import HTTPException
from sqlalchemy.orm import Session

def criar_doutor(db: Session, doutor: DoutorCreate):
    try:
        print(f'Doutor recebido: {doutor}')

        # Criptografa a senha
        senha_hash = gerar_hash(doutor.senha)
        print(f'Senha criptografada: {senha_hash}')

        # Cria a pessoa
        nova_pessoa = Pessoa(
            nome=doutor.nome,
            contato=doutor.contato,
            email=doutor.email,
            senha_criptografada=senha_hash
        )
        db.add(nova_pessoa)
        db.commit()  # Commit da pessoa
        db.refresh(nova_pessoa)  # Atualiza a pessoa com o ID gerado
        print(f'Pessoa criada com ID: {nova_pessoa.pessoa_id}')

        # Cria o doutor usando o ID da pessoa
        novo_doutor = Doutor(
            doutor_id=nova_pessoa.pessoa_id,  # usa o ID da pessoa
            nome=doutor.nome,
            contato=doutor.contato,
            email=doutor.email,
            senha_criptografada=senha_hash,
            especializacao=doutor.especializacao
        )

        db.add(novo_doutor)
        db.commit()  
        db.refresh(novo_doutor)  

        # Retorna o doutor com status 200
        return novo_doutor

    except Exception as e:
        print(f'Erro ao criar doutor: {e}')
        raise HTTPException(status_code=500, detail=f"Erro interno ao criar doutor: {str(e)}")


from fastapi import HTTPException

def excluir_doutor(db: Session, doutor_id: int):
    doutor = buscar_doutor(db, doutor_id)

    if not doutor:
        raise HTTPException(status_code=404, detail="Doutor não encontrado.")

    try:
        if doutor:
            print('Pessoa a ser deletada: ', doutor)
            db.delete(doutor) 
            db.commit()
            raise HTTPException(status_code=500, detail=f"Doutor excluído com sucesso!")
        else:
            raise HTTPException(status_code=404, detail="Pessoa vinculada ao doutor não encontrada.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao excluir doutor: {str(e)}")





