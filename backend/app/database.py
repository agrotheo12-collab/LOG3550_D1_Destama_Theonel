from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine


# Chemin de la base de données SQLite
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "bibliotheque.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

# Configuration du moteur SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)


def creer_tables():
    """Créer les tables définies dans les modèles SQLModel."""
    from app.models import Livre

    SQLModel.metadata.create_all(engine)


def get_session():
    """Fournir une session de base de données pour chaque requête."""
    with Session(engine) as session:
        yield session
