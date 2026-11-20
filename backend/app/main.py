from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import creer_tables
from app.routers.livres import router as livres_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialiser la base de données au démarrage de l'application."""
    creer_tables()
    yield


app = FastAPI(
    title="API Bibliothèque",
    description=(
        "API REST de gestion d'une bibliothèque. "
        "Elle permet de créer, consulter, rechercher, modifier "
        "et supprimer des livres."
    ),
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(livres_router)


@app.get(
    "/sante",
    tags=["Système"],
    summary="Vérifier l'état de l'API",
    description="Indique si l'API fonctionne correctement."
)
def verifier_sante():
    return {"statut": "ok"}
