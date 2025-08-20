from typing import Union
from pydantic import BaseModel
from sqlalchemy import Date

# Price
class PriceBase(BaseModel):
    valeur: int|float
    
class PriceOut(PriceBase):
    
    class Config:
        orm_mode = True

# Inventaire
class FruitBase(BaseModel):
    name: str
    quantite: int|float

    
class FruitInventaire(FruitBase):
    id: int
    

class FruitCreate(FruitBase):
    prix: int|float
    
class FruitOut(FruitBase):
    id: int
    prix: PriceOut

    class Config:
        orm_mode = True

# Sales
class SaleBase(BaseModel):
    name_fruit: str
    quantite: int
    # prix_total: int|float
    
    class Config:
        orm_mode = True
    