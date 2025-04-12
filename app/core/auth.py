from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.pessoa_model import Pessoa

SECRET_KEY = "segredo_muito_secreto"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

from passlib.context import CryptContext

# Criação do contexto para criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_token(pessoa: Pessoa):
    expira = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(pessoa.pessoa_id),
        "nome": pessoa.nome,
        "email": pessoa.email,
        "funcao": pessoa.funcao,
        "exp": expira
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Pessoa:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        pessoa_id = int(payload.get("sub"))
        pessoa = db.query(Pessoa).filter(Pessoa.pessoa_id == pessoa_id).first()
        if pessoa is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return pessoa
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

def usuario_admin(pessoa: Pessoa = Depends(verificar_token)):
    if pessoa.funcao != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return pessoa

def usuario_doutor(pessoa: Pessoa = Depends(verificar_token)):
    if pessoa.funcao != "doutor":
        raise HTTPException(status_code=403, detail="Acesso restrito a doutores")
    return pessoa

def usuario_paciente(pessoa: Pessoa = Depends(verificar_token)):
    if pessoa.funcao != "paciente":
        raise HTTPException(status_code=403, detail="Acesso restrito a pacientes")
    return pessoa

def gerar_hash(senha):
    return pwd_context.hash(senha)

def verificar_senha(senha_plain, senha_hash):
    return pwd_context.verify(senha_plain, senha_hash)