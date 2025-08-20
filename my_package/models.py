from typing import List, Union
from typing import Optional
from sqlalchemy import ForeignKey, null
from sqlalchemy import String, Integer, Float, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

# CREATION BASE DE DONNEE
class Base(DeclarativeBase):
    pass

class Inventaire(Base):
    __tablename__ = "inventaire" # Nom de la table
    
    # attribut de chaque colonne
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30),unique=True, index=True, nullable=False)
    quantite: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    prix: Mapped["Price"] = relationship(back_populates='inventaire', uselist=False)
    
    def __repr__(self) -> str:
        return f"iventaire(id={self.id!r}, name={self.name!r}, quantite={self.quantite!r})"

class Price(Base):
    # Nom de la table
    __tablename__="prices"
    
    # attribut de chaque colonne
    id: Mapped[int] = mapped_column(ForeignKey("inventaire.id"), primary_key=True, index=True, unique=True)
    valeur: Mapped[float] = mapped_column(Float, nullable=False)
    
    inventaire: Mapped["Inventaire"] = relationship(back_populates="prix")
    
    def __repr__(self) -> str:
        return f"Price(id={self.id!r}, valeur={self.valeur!r})"
    
class History(Base):
    __tablename__="history"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    id_fruit: Mapped[int] = mapped_column(Integer, ForeignKey("inventaire.id"), nullable=False)
    nombre: Mapped[int] = mapped_column(Integer, nullable=False)
    prix_total: Mapped[float] = mapped_column(Float, nullable=False)

