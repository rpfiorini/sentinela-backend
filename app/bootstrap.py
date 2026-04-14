from app.core.db import Base, engine, SessionLocal
from app.models.models import Company

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if not db.query(Company).first():
            db.add(Company(name="Sentinela Operacional", cnpj=""))
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    run()
