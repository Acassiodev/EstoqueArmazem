
from sqlalchemy.orm import Session
from app.models import category_model
from app.schemas import category_schema

def get_category_by_name(db: Session, name: str):
    return db.query(category_model.Category).filter(category_model.Category.name == name).first()

def get_category(db: Session, category_id: int):
    return db.query(category_model.Category).filter(category_model.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(category_model.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: category_schema.CategoryCreate):
    db_category = category_model.Category(name=category.name)
    db.add(db_category)
    db.commit() # Operação atômica
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category: category_model.Category):
    db.delete(category)
    db.commit() # Operação atômica
    return category

def update_category(db: Session, category: category_model.Category, update_data: category_schema.CategoryCreate):
    category.name = update_data.name
    db.commit()
    db.refresh(category)
    return category