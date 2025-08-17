from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import select
import os
from fruit_manager import ouvrir_inventaire, ouvrir_prix

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
    # name_id:Mapped[int] = mapped_column()
    
    inventaire: Mapped["Inventaire"] = relationship(back_populates="prix")
    
    def __repr__(self) -> str:
        return f"Price(id={self.id!r}, price={self.price!r})"
    

    
# FONCTION
def create_db():
    Base.metadata.create_all(engine)


def importation_json_to_db():
    inventaire = ouvrir_inventaire()
    dict_prix = ouvrir_prix()
    id = 1
    
    with Session(engine) as session:
        elements_inventaire = []
        elements_price = []
        
        for name, quantite in inventaire.items():
            element_inventaire = Inventaire(
                                                id=id,
                                                name=name,
                                                quantite=quantite,
                                                prix=Price(price=float(dict_prix.get(name)))
                                            )
            # element_price = Price(
            #                         id=id,
            #                         price=prix.get(name),
            #                         name_id=id
            #                     )
            id+=1
    
            elements_inventaire.append(element_inventaire)
            # elements_price.append(element_price)
        # Ajoute     
        session.add_all(elements_inventaire)
        # session.add_all(elements_price)
        
        session.commit()
        
# def recolte(name):
    

        
if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    db_path = os.path.join(base_dir, 'inventaire.db')
    engine = create_engine(f"sqlite:///data/database.db", echo=True)

    if os.path.exists("data/inventaire.db"):
        os.remove("data/inventaire.db")
    create_db()
    importation_json_to_db()