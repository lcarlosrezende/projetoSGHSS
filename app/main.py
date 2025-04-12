from fastapi import FastAPI
from app.views import pessoa_view
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SGHSS - API")

app.include_router(pessoa_view.router, prefix="/api", tags=["Pessoas"])
