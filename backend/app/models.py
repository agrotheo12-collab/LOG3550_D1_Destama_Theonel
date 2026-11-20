from enum import Enum
from typing import Optional

from sqlalchemy import Column, Enum as SQLAlchemyEnum
from sqlmodel import Field, SQLModel


class Categorie(str, Enum):
    ROMAN = "roman"
    SCIENCE = "science"
    HISTOIRE = "histoire"
    INFORMATIQUE = "informatique"
    AUTRE = "autre"


class Livre(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    titre: str = Field(
        min_length=2,
        max_length=200,
        index=True
    )

    auteur: str = Field(
        min_length=2,
        max_length=200,
        index=True
    )

    annee: int

    categorie: Categorie = Field(
        sa_column=Column(
            SQLAlchemyEnum(
                Categorie,
                values_callable=lambda enum_cls: [
                    item.value for item in enum_cls
                ]
            ),
            nullable=False
        )
    )

    isbn: Optional[str] = Field(
        default=None,
        unique=True,
        index=True,
        max_length=13
    )

    disponible: bool = Field(default=True)
