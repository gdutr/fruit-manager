from typing import List, Union
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
from models import Base, Inventaire, Price

######################
    
# FONCTION

######################
def create_db():
    if os.path.exists("data/database.db"):
        os.remove("data/database.db")
    Base.metadata.create_all(engine)


def importation_json_to_db():
    inventaire = ouvrir_inventaire()
    dict_prix = ouvrir_prix()
    id = 1
    
    with Session(engine) as session:
        elements_inventaire = []
         
        for name, quantite in inventaire.items():
            element_inventaire = Inventaire(
                                                # id=id,
                                                name=name,
                                                quantite=quantite,
                                                prix=Price(valeur=float(dict_prix.get(name)))
                                            )

            id+=1
    
            elements_inventaire.append(element_inventaire)
            # elements_price.append(element_price)
        # Ajoute     
        session.add_all(elements_inventaire)
         
        session.commit()
        
def recolte(name:str, quantite:int):
    engine = create_engine(f"sqlite:///data/database.db", echo=True)
    with Session(engine) as session:
        stmt = select(Inventaire).where(Inventaire.name == name)
        fruit = session.scalars(stmt).one()
        fruit.quantite += quantite
        print(fruit.quantite)
        session.commit()
 

        
if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    db_path = os.path.join(base_dir, 'database.db')
    engine = create_engine(f"sqlite:///data/database.db", echo=True)

    create_db()
    importation_json_to_db()