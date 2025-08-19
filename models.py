from typing import List, Union
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# CREATION BASE DE DONNEE
class Base(DeclarativeBase):
    pass

class Inventaire(Base):
    # Nom de la table
    __tablename__ = "inventaire"
    # attribut de chaque colonne
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    quantite: Mapped[float] = mapped_column(nullable=False)
    
    prix: Mapped["Price"] = relationship(back_populates='inventaire')
    
    def __repr__(self) -> str:
        return f"iventaire(id={self.id!r}, name={self.name!r}, quantite={self.quantite!r})"

class Price(Base):
    # Nom de la table
    __tablename__="prices"
    
    # attribut de chaque colonne
    id: Mapped[int] = mapped_column(ForeignKey("inventaire.id"),primary_key=True)
    price: Mapped[float] = mapped_column(nullable=False)
    
    inventaire: Mapped["Inventaire"] = relationship(back_populates="prix")
    
    def __repr__(self) -> str:
        return f"Price(id={self.id!r}, price={self.price!r})"
    
