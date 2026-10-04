import os
from contextlib import contextmanager
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import Column, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, joinedload

env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    fruits = relationship("Fruit", back_populates="category")

class Fruit(Base):
    __tablename__ = "fruits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    category = relationship("Category", back_populates="fruits")

@contextmanager
def get_db():
    """Database session context manager"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def get_all_categories():
    with get_db() as db:
        return db.query(Category).order_by(Category.id).all()

def get_category_by_id(category_id: int):
    with get_db() as db:
        return db.query(Category).filter(Category.id == category_id).first()

def create_category(cat_data):
    with get_db() as db:
        cat = Category(name=cat_data.name)
        db.add(cat)
        db.commit()
        db.refresh(cat)
        return cat

def update_category(category_id: int, cat_data):
    with get_db() as db:
        cat = db.query(Category).filter(Category.id == category_id).first()
        if not cat:
            return None
        cat.name = cat_data.name
        db.commit()
        db.refresh(cat)
        return cat

def delete_category(category_id: int):
    with get_db() as db:
        cat = db.query(Category).filter(Category.id == category_id).first()
        if not cat:
            return 0
        linked = db.query(Fruit).filter(Fruit.category_id == category_id).first()
        if linked:
            return {"error": "Category has linked fruits; delete or reassign them first.", "id": category_id}
        db.delete(cat)
        db.commit()
        return 1

def get_all_fruits():
    with get_db() as db:
        return db.query(Fruit).options(joinedload(Fruit.category)).order_by(Fruit.id).all()

def get_fruit_by_id(fruit_id: int):
    with get_db() as db:
        return db.query(Fruit).options(joinedload(Fruit.category)).filter(Fruit.id == fruit_id).first()

def create_fruit(fruit_data):
    with get_db() as db:
        fruit = Fruit(
            name=fruit_data.name,
            category_id=fruit_data.category_id,
            price=fruit_data.price,
            quantity=fruit_data.quantity,
        )
        db.add(fruit)
        db.commit()
        db.refresh(fruit)
        db.refresh(fruit, attribute_names=["category"])
        return db.query(Fruit).options(joinedload(Fruit.category)).filter(Fruit.id == fruit.id).first()

def update_fruit(fruit_id: int, fruit_data):
    with get_db() as db:
        fruit = db.query(Fruit).options(joinedload(Fruit.category)).filter(Fruit.id == fruit_id).first()
        if not fruit:
            return None
        fruit.name = fruit_data.name
        fruit.category_id = fruit_data.category_id
        fruit.price = fruit_data.price
        fruit.quantity = fruit_data.quantity
        db.commit()
        db.refresh(fruit)
        return db.query(Fruit).options(joinedload(Fruit.category)).filter(Fruit.id == fruit_id).first()

def delete_fruit(fruit_id: int):
    with get_db() as db:
        fruit = db.query(Fruit).filter(Fruit.id == fruit_id).first()
        if not fruit:
            return 0
        db.delete(fruit)
        db.commit()
        return 1