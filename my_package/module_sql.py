from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    pass

class Inventaire(Base):
    # Nom de la table
    __tablename__ = "inventaire"
    # attribut de chaque colonne
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    quantite: Mapped[int] = mapped_column(nullable=False)
    
    prix: Mapped[List["Price"]] = relationship(
        back_populates='price', cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"iventaire(id={self.id!r}, name={self.name!r}, quantite={self.quantite!r})"

class Price(Base):
    # Nom de la table
    __tablename__="prices"
    
    # attribut de chaque colonne
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(nullable=False)
    name_id:Mapped[int] = mapped_column(ForeignKey("inventaire.id"))
    
    def __repr__(self) -> str:
        return f"Price(id={self.id!r}, price={self.price!r})"
    
if __name__ == "__main__":
    engine = create_engine("sqlite:///SQL/inventaire.db", echo=True)
    
    # Création des tables
    Base.metadata.create_all(engine)