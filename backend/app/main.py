from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import creer_tables, initialiser_donnees
from app.routers.livres import router as livres_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialiser la base de données au démarrage de l'application."""
    creer_tables()
    initialiser_donnees()
    yield


app = FastAPI(
    title="API Bibliothèque du Collège Sainte Croix de Limbé",
    description=(
        "API REST de gestion de la bibliothèque du Collège Sainte Croix de Limbé. "
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
