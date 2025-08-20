from typing import Union
from pydantic import BaseModel
from sqlalchemy import Date

# Price
class PriceBase(BaseModel):
    valeur: int|float
    
class PriceOut(PriceBase):
    
    class Config:
        from_attributes  = True

# Inventaire
class FruitBase(BaseModel):
    name: str
    quantite: int|float

    
class FruitInventaire(FruitBase):
    id: int
    

class FruitCreate(FruitBase):
    prix: int|float
    
class FruitOut(BaseModel):
    id: int
    name: str
    quantite: int
    prix: PriceOut    

    # class Config:
    #     from_attributes  = True

class InventaireOut(BaseModel):
    id: int
    name: str
    quantite: int
    # pas de prix ici pour éviter la recursion

    class Config:
        from_attributes = True


# Sales
class SaleBase(BaseModel):
    name_fruit: str
    quantite: int
    # prix_total: int|float
    
    class Config:
        from_attributes  = True
        

    