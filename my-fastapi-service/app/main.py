from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://lab_user:lab_password@db:3306/lab_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Mesteri Labor 2 - Adatbazis csatlakoztatva"}

@app.post("/items/")
def create_item(name: str):
    db = SessionLocal()
    new_item = Item(name=name)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    db.close()
    return new_item

@app.get("/items/")
def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

@app.get("/health")
def health_check():
    return {"status": "ok"}
