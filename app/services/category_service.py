# Crie um arquivo app/services/category_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories import category_repository
from app.schemas import category_schema

def create_new_category(db: Session, category: category_schema.CategoryCreate):
    # REGRA DE NEGÓCIO (RF004): Nome de categoria deve ser único
    existing_category = category_repository.get_category_by_name(db, name=category.name)
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists",
        )
    return category_repository.create_category(db=db, category=category)

def remove_category(db: Session, category_id: int):
    category_to_delete = category_repository.get_category(db, category_id)
    if not category_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    # REGRA DE NEGÓCIO (RF004): Não permitir exclusão de categoria com produtos vinculados
    if category_to_delete.products: # Se a lista de produtos não estiver vazia
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with associated products",
        )
        
        

def update_existing_category(db: Session, category_id: int, category_update: category_schema.CategoryCreate):
    category_to_update = category_repository.get_category(db, category_id)
    if not category_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    # Verifica se o novo nome já está em uso por outra categoria
    existing_category_with_name = category_repository.get_category_by_name(db, name=category_update.name)
    if existing_category_with_name and existing_category_with_name.id != category_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already in use")

    return category_repository.update_category(db, category_to_update, category_update)
        

    return category_repository.delete_category(db, category_to_delete)