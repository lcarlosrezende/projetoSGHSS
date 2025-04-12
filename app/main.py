from fastapi import FastAPI
from app.views import pessoa_view, paciente_view
from app.core.database import Base, engine
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SGHSS - API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SGHSS - API",
        version="1.0.0",
        description="Sistema de Gestão Hospitalar e de Serviços de Saúde",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if "security" not in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Rotas
app.include_router(pessoa_view.router, prefix="/api", tags=["Pessoas"])
app.include_router(paciente_view.router, prefix="/api/pacientes", tags=["Pacientes"])
