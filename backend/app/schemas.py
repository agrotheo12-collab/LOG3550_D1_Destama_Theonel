from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models import Categorie


ANNEE_ACTUELLE = date.today().year


class LivreBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titre: str = Field(min_length=2, max_length=200)
    auteur: str = Field(min_length=2, max_length=200)
    annee: int = Field(ge=1450, le=ANNEE_ACTUELLE)
    categorie: Categorie
    isbn: Optional[str] = None
    disponible: bool = True

    @field_validator("isbn")
    @classmethod
    def valider_isbn(cls, valeur):
        if valeur is not None and (
            not valeur.isdigit() or len(valeur) not in (10, 13)
        ):
            raise ValueError(
                "L'ISBN doit contenir exactement 10 ou 13 chiffres."
            )
        return valeur


class LivreCreate(LivreBase):
    pass


class LivreUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titre: Optional[str] = Field(default=None, min_length=2, max_length=200)
    auteur: Optional[str] = Field(default=None, min_length=2, max_length=200)
    annee: Optional[int] = Field(
        default=None, ge=1450, le=ANNEE_ACTUELLE
    )
    categorie: Optional[Categorie] = None
    isbn: Optional[str] = None
    disponible: Optional[bool] = None

    @field_validator("isbn")
    @classmethod
    def valider_isbn(cls, valeur):
        if valeur is not None and (
            not valeur.isdigit() or len(valeur) not in (10, 13)
        ):
            raise ValueError(
                "L'ISBN doit contenir exactement 10 ou 13 chiffres."
            )
        return valeur


class LivreRead(LivreBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )
