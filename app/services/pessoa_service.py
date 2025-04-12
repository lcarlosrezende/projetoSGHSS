from sqlalchemy.orm import Session
from app.models.pessoa_model import Pessoa
from app.repositories import pessoa_repository
from app.core.auth import gerar_hash, criar_token, verificar_senha

def registrar_usuario(db: Session, nome, email, senha, contato):
    if pessoa_repository.buscar_por_email(db, email):
        return None, "Usuário já existe."
    senha_hash = gerar_hash(senha)
    nova_pessoa = Pessoa(nome=nome, email=email, senha_criptografada=senha_hash, contato=contato)
    pessoa = pessoa_repository.criar_pessoa(db, nova_pessoa)
    return pessoa, None

def autenticar_usuario(db: Session, email: str, senha: str):
    pessoa = pessoa_repository.buscar_por_email(db, email)
    if not pessoa or not verificar_senha(senha, pessoa.senha_criptografada):
        return None
    token = criar_token({"sub": str(pessoa.pessoa_id)})
    pessoa.token_de_acesso = token
    db.commit()
    return token
