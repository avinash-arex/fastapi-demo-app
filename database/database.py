from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:123456789@localhost:5432/fastAPI"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close
