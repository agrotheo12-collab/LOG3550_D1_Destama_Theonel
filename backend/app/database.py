from pathlib import Path

from sqlmodel import Session, SQLModel, create_engine, select


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


def initialiser_donnees():
    """Insérer les dix livres initiaux si la bibliothèque est vide."""
    from app.models import Categorie, Livre

    livres_initiaux = [
        Livre(
            titre="Le Petit Prince",
            auteur="Antoine de Saint-Exupéry",
            annee=1943,
            categorie=Categorie.LITTERATURE,
            disponible=True
        ),
        Livre(
            titre="Les Misérables",
            auteur="Victor Hugo",
            annee=1862,
            categorie=Categorie.ROMAN,
            disponible=True
        ),
        Livre(
            titre="L'Étranger",
            auteur="Albert Camus",
            annee=1942,
            categorie=Categorie.ROMAN,
            disponible=False
        ),
        Livre(
            titre="Les Arbres musiciens",
            auteur="Jacques Stephen Alexis",
            annee=1957,
            categorie=Categorie.SCIENCE_FICTION,
            disponible=True
        ),
        Livre(
            titre="Gouverneurs de la rosée",
            auteur="Jacques Roumain",
            annee=1944,
            categorie=Categorie.LITTERATURE,
            disponible=True
        ),
        Livre(
            titre="Histoire d'Haïti",
            auteur="Thomas Madiou",
            annee=1847,
            categorie=Categorie.HISTOIRE,
            disponible=False
        ),
        Livre(
            titre="Clean Code",
            auteur="Robert C. Martin",
            annee=2008,
            categorie=Categorie.INFORMATIQUE,
            disponible=True
        ),
        Livre(
            titre="La Bible",
            auteur="Collectif d'auteurs",
            annee=1450,
            categorie=Categorie.RELIGION,
            disponible=True
        ),
        Livre(
            titre="Dézafi",
            auteur="Frankétienne",
            annee=1975,
            categorie=Categorie.LANGUE,
            disponible=True
        ),
        Livre(
            titre="L'Espace d'un cillement",
            auteur="Jacques Stephen Alexis",
            annee=1959,
            categorie=Categorie.LITTERATURE,
            disponible=True
        )
    ]

    with Session(engine) as session:
        livres_existants = session.exec(select(Livre)).first()

        if livres_existants is None:
            session.add_all(livres_initiaux)
            session.commit()