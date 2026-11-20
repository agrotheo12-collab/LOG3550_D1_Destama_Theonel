import pytest

from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.database import get_session
from app.main import app


@pytest.fixture
def moteur_test():
    """Créer une base de données SQLite temporaire pour les tests."""
    moteur = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    SQLModel.metadata.create_all(moteur)

    yield moteur

    SQLModel.metadata.drop_all(moteur)
    moteur.dispose()


@pytest.fixture
def client(moteur_test):
    """Créer un client de test utilisant uniquement la base temporaire."""

    def session_test():
        with Session(moteur_test) as session:
            yield session

    app.dependency_overrides[get_session] = session_test

    client_test = TestClient(app)

    yield client_test

    app.dependency_overrides.clear()


def donnees_livre():
    """Fournir les données d'un livre valide."""
    return {
        "titre": "Introduction a Linux",
        "auteur": "Theonel Destama",
        "annee": 2022,
        "categorie": "Informatique",
        "isbn": "9781234567897",
        "disponible": True
    }


def test_creer_livre(client):
    """Vérifier la création d'un livre."""
    reponse = client.post("/livres/", json=donnees_livre())

    assert reponse.status_code == 201
    assert reponse.json()["titre"] == "Introduction a Linux"
    assert reponse.json()["id"] is not None
    assert reponse.headers["location"].startswith("/livres/")


def test_obtenir_livre(client):
    """Vérifier la consultation d'un livre par son identifiant."""
    creation = client.post("/livres/", json=donnees_livre())
    livre_id = creation.json()["id"]

    reponse = client.get(f"/livres/{livre_id}")

    assert reponse.status_code == 200
    assert reponse.json()["id"] == livre_id
    assert reponse.json()["titre"] == "Introduction a Linux"


def test_lister_livres_avec_filtres(client):
    """Vérifier la recherche et les filtres de la liste des livres."""
    client.post("/livres/", json=donnees_livre())

    autre_livre = donnees_livre()
    autre_livre.update({
        "titre": "Histoire d'Haiti",
        "auteur": "Thomas Madiou",
        "annee": 1847,
        "categorie": "Histoire",
        "isbn": None,
        "disponible": False
    })
    client.post("/livres/", json=autre_livre)

    reponse = client.get(
        "/livres/",
        params={
            "q": "Destama",
            "categorie": "Informatique",
            "disponible": "true"
        }
    )

    assert reponse.status_code == 200
    assert len(reponse.json()) == 1
    assert reponse.json()[0]["auteur"] == "Theonel Destama"


def test_remplacer_livre(client):
    """Vérifier le remplacement complet d'un livre avec PUT."""
    creation = client.post("/livres/", json=donnees_livre())
    livre_id = creation.json()["id"]

    nouvelles_donnees = {
        "titre": "Programmation avec Python",
        "auteur": "Theonel Destama",
        "annee": 2024,
        "categorie": "Informatique",
        "isbn": None,
        "disponible": False
    }

    reponse = client.put(
        f"/livres/{livre_id}",
        json=nouvelles_donnees
    )

    assert reponse.status_code == 200
    assert reponse.json()["titre"] == "Programmation avec Python"
    assert reponse.json()["disponible"] is False


def test_modifier_partiellement_livre(client):
    """Vérifier la modification partielle d'un livre avec PATCH."""
    creation = client.post("/livres/", json=donnees_livre())
    livre_id = creation.json()["id"]

    reponse = client.patch(
        f"/livres/{livre_id}",
        json={"disponible": False}
    )

    assert reponse.status_code == 200
    assert reponse.json()["disponible"] is False
    assert reponse.json()["titre"] == "Introduction a Linux"


def test_supprimer_livre(client):
    """Vérifier la suppression d'un livre."""
    creation = client.post("/livres/", json=donnees_livre())
    livre_id = creation.json()["id"]

    reponse = client.delete(f"/livres/{livre_id}")

    assert reponse.status_code == 204

    verification = client.get(f"/livres/{livre_id}")
    assert verification.status_code == 404


def test_livre_introuvable(client):
    """Vérifier la réponse 404 pour un livre inexistant."""
    reponse = client.get("/livres/9999")

    assert reponse.status_code == 404
    assert reponse.json()["detail"] == "Livre introuvable."


def test_validation_donnees_invalides(client):
    """Vérifier le rejet des données invalides."""
    donnees = donnees_livre()
    donnees["titre"] = "A"
    donnees["annee"] = 1400

    reponse = client.post("/livres/", json=donnees)

    assert reponse.status_code == 422


def test_validation_categorie_et_isbn(client):
    """Vérifier le rejet d'une catégorie et d'un ISBN invalides."""
    donnees = donnees_livre()
    donnees["categorie"] = "Geographie"

    reponse_categorie = client.post("/livres/", json=donnees)
    assert reponse_categorie.status_code == 422

    donnees = donnees_livre()
    donnees["isbn"] = "12345"

    reponse_isbn = client.post("/livres/", json=donnees)
    assert reponse_isbn.status_code == 422


def test_isbn_duplique(client):
    """Vérifier le rejet d'un ISBN déjà enregistré."""
    donnees = donnees_livre()

    premiere_reponse = client.post("/livres/", json=donnees)
    assert premiere_reponse.status_code == 201

    donnees["titre"] = "Autre livre informatique"

    seconde_reponse = client.post("/livres/", json=donnees)

    assert seconde_reponse.status_code == 409
    assert seconde_reponse.json()["detail"] == (
        "Un livre avec cet ISBN existe déjà."
    )


def test_verifier_sante_api(client):
    """Vérifier le fonctionnement de l'API."""
    reponse = client.get("/sante")

    assert reponse.status_code == 200
    assert reponse.json() == {"statut": "ok"}


def test_rejeter_identifiant_fourni_par_client(client):
    """Vérifier que le client ne peut pas fournir son propre identifiant."""
    donnees = donnees_livre()
    donnees["id"] = 99

    reponse_creation = client.post("/livres/", json=donnees)

    assert reponse_creation.status_code == 422

    creation = client.post("/livres/", json=donnees_livre())
    livre_id = creation.json()["id"]

    reponse_modification = client.patch(
        f"/livres/{livre_id}",
        json={"id": 99}
    )

    assert reponse_modification.status_code == 422
