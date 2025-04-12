from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "124578"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gerar_hash(senha):
    return pwd_context.hash(senha)

def verificar_senha(senha_plain, senha_hash):
    return pwd_context.verify(senha_plain, senha_hash)

def criar_token(dados: dict):
    dados_token = dados.copy()
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_token.update({"exp": exp})
    return jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
