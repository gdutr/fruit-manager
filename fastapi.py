from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from my_package.models import Base, Inventaire, Price, History
from my_package.database import engine, get_db
from my_package.schemas import FruitCreate, FruitInventaire, FruitBase, FruitOut, SaleBase, InventaireOut
from datetime import datetime


app = FastAPI()

# Créer les tables si elles n'existent pas encore
Base.metadata.create_all(bind=engine)

# VARIABLE
# db = Depends(get_db)
# fruit_tuple = db.query(Inventaire.name).all()
# # transformation en liste
# FRUIT_LIST = [fruit[0] for fruit in fruit_tuple]

##########################

# INVENTAIRE

##########################

@app.get("/inventaire/", response_model=list[FruitInventaire])
async def inventaire(db:Session = Depends(get_db)):
    return db.query(Inventaire).all()


@app.get("/inventaire/{fruit}", response_model = FruitInventaire)
async def fruit(fruit:str, db:Session = Depends(get_db)):
    query = db.query(Inventaire).where(Inventaire.name==fruit).one()
    if not query:
        raise HTTPException(status_code=404, detail='Le fruit ne se trouve pas dans la base de donnée')
    else:
        return query


@app.post("/inventaire/vente/")
async def sell_fruit(fruit: SaleBase, db: Session = Depends(get_db)):
    query_fruit = db.query(Inventaire).where(Inventaire.name==fruit.name_fruit).first()
    if query_fruit is None:
        raise HTTPException(status_code=404, detail='Le fruit ne se trouve pas dans la base de donnée')
    # PRIX
    prix = db.query(Price.valeur).join(Inventaire).where(Inventaire.name==fruit.name_fruit).one()[0]
    
    # CREATION HISTORY
    history_fruit = History(
        date = datetime.now(),#.strftime("%d/%m/%Y, %H:%M:%S"),
        name_fruit = query_fruit.name,
        nombre = fruit.quantite,
        prix_total = fruit.quantite * prix
    )
    
    db.add(history_fruit)
    
    # Mise à jour
    query_fruit.quantite -= fruit.quantite
    db.commit()
    db.refresh(history_fruit)
    db.refresh(query_fruit)
    return query_fruit


@app.put("/inventaire/recolte/{fruit}")
async def harvest_fruit(fruit: str, value: int, db: Session = Depends(get_db)):
    query_fruit = db.query(Inventaire).where(Inventaire.name==fruit).first()
    if query_fruit is None:
        raise HTTPException(status_code=404, detail='Le fruit ne se trouve pas dans la base de donnée')
    
    # Mise à jour
    query_fruit.quantite += value
    db.commit()
    db.refresh(query_fruit)
    return query_fruit



@app.post("/inventaire/newfruit/", response_model=FruitOut)
async def create_fruit(fruit: FruitCreate, db: Session = Depends(get_db)):
    db_fruit = Inventaire(
        name=fruit.name, 
        quantite=fruit.quantite, 
        prix=Price(valeur=fruit.prix)
        )
    db.add(db_fruit)
    db.commit()
    db.refresh(db_fruit)
    return db_fruit


@app.delete("/inventaire/delete/{fruit}", response_model=InventaireOut)
async def delete_fruit(fruit:str, db:Session = Depends(get_db)):
    query_fruit = db.query(Inventaire).where(Inventaire.name==fruit).first()
    print(query_fruit)
    if query_fruit: 
        db.delete(query_fruit)
        db.commit()
        return query_fruit
    raise HTTPException(status_code=404, detail='Le fruit ne se trouve pas dans la base de donnée')



# @app.post("/users/", response_model=FruitCreate)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = User(name=user.name, email=user.email)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user



# @app.get("/users/", response_model=list[UserRead])
# def list_users(db: Session = Depends(get_db)):
#     return db.query(User).all()
