from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///data/database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()  # Crée une session SQLAlchemy (connexion à la base)
    try:
        yield db  # Donne cette session à la fonction ou route FastAPI qui en a besoin
    finally:
        db.close()  # Ferme la session à la fin de l’utilisation (libère les ressources)
        
if __name__ == '__main__':
    print(get_db())