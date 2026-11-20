from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import creer_tables, initialiser_donnees
from app.routers.livres import router as livres_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialiser la base de données au démarrage de l'application."""
    creer_tables()
    initialiser_donnees()
    yield


descriptions_tags = [
    {
        "name": "Livres",
        "description": (
            "Opérations de gestion du catalogue de livres : "
            "ajout, consultation, recherche, modification et suppression."
        ),
    },
    {
        "name": "Système",
        "description": (
            "Opérations permettant de vérifier le fonctionnement de l'API."
        ),
    },
]


app = FastAPI(
    title="API Bibliothèque du Collège Sainte Croix de Limbé",
    description=(
        "API REST de gestion de la bibliothèque du Collège Sainte Croix de Limbé. "
        "Elle permet de créer, consulter, rechercher, modifier "
        "et supprimer des livres."
    ),
    version="1.0.0",
    openapi_tags=descriptions_tags,
    lifespan=lifespan
)


# Autoriser uniquement le frontend de l'application.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
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
