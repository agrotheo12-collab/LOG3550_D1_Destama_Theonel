from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.database import get_session
from app.models import Categorie, Livre
from app.schemas import LivreCreate, LivreRead, LivreUpdate


router = APIRouter(
    prefix="/livres",
    tags=["Livres"]
)


@router.get("/", response_model=list[LivreRead])
def lister_livres(
    q: Optional[str] = Query(default=None, description="Recherche par titre ou auteur"),
    categorie: Optional[Categorie] = Query(default=None, description="Filtrer par catégorie"),
    disponible: Optional[bool] = Query(default=None, description="Filtrer par disponibilité"),
    skip: int = Query(default=0, ge=0, description="Nombre de livres à ignorer"),
    limit: int = Query(default=20, ge=1, le=100, description="Nombre maximum de livres"),
    session: Session = Depends(get_session)
):
    requete = select(Livre)

    if q:
        recherche = f"%{q}%"
        requete = requete.where(
            or_(
                Livre.titre.ilike(recherche),
                Livre.auteur.ilike(recherche)
            )
        )

    if categorie is not None:
        requete = requete.where(Livre.categorie == categorie)

    if disponible is not None:
        requete = requete.where(Livre.disponible == disponible)

    requete = requete.offset(skip).limit(limit)

    return session.exec(requete).all()


@router.get("/{livre_id}", response_model=LivreRead)
def obtenir_livre(
    livre_id: int,
    session: Session = Depends(get_session)
):
    livre = session.get(Livre, livre_id)

    if livre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre introuvable."
        )

    return livre


@router.post(
    "/",
    response_model=LivreRead,
    status_code=status.HTTP_201_CREATED
)
def creer_livre(
    donnees: LivreCreate,
    response: Response,
    session: Session = Depends(get_session)
):
    livre = Livre.model_validate(donnees)

    session.add(livre)

    try:
        session.commit()
        session.refresh(livre)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un livre avec cet ISBN existe déjà."
        )

    response.headers["Location"] = f"/livres/{livre.id}"

    return livre


@router.put("/{livre_id}", response_model=LivreRead)
def remplacer_livre(
    livre_id: int,
    donnees: LivreCreate,
    session: Session = Depends(get_session)
):
    livre = session.get(Livre, livre_id)

    if livre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre introuvable."
        )

    livre.titre = donnees.titre
    livre.auteur = donnees.auteur
    livre.annee = donnees.annee
    livre.categorie = donnees.categorie
    livre.isbn = donnees.isbn
    livre.disponible = donnees.disponible

    try:
        session.add(livre)
        session.commit()
        session.refresh(livre)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un livre avec cet ISBN existe déjà."
        )

    return livre


@router.patch("/{livre_id}", response_model=LivreRead)
def modifier_livre(
    livre_id: int,
    donnees: LivreUpdate,
    session: Session = Depends(get_session)
):
    livre = session.get(Livre, livre_id)

    if livre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre introuvable."
        )

    modifications = donnees.model_dump(exclude_unset=True)

    for champ, valeur in modifications.items():
        setattr(livre, champ, valeur)

    try:
        session.add(livre)
        session.commit()
        session.refresh(livre)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un livre avec cet ISBN existe déjà."
        )

    return livre


@router.delete(
    "/{livre_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def supprimer_livre(
    livre_id: int,
    session: Session = Depends(get_session)
):
    livre = session.get(Livre, livre_id)

    if livre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre introuvable."
        )

    session.delete(livre)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
