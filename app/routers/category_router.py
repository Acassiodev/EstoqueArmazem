from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import category_schema
from app.services import category_service
from app.repositories import category_repository

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# RF001 - Criar categoria com nome único
@router.post("/", response_model=category_schema.Category, status_code=status.HTTP_201_CREATED)
def create_category(category: category_schema.CategoryCreate, db: Session = Depends(get_db)):
    # O logging deve ser adicionado aqui
    return category_service.create_new_category(db=db, category=category)

# RF001 - Listar todas as categorias
@router.get("/", response_model=List[category_schema.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = category_repository.get_categories(db, skip=skip, limit=limit)
    return categories

# RF001 - Buscar categoria por ID
@router.get("/{category_id}", response_model=category_schema.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = category_repository.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# RF001 - Excluir categoria
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    # O logging deve ser adicionado aqui
    category_service.remove_category(db=db, category_id=category_id)
    return



# RF001 - Atualizar dados da categoria
@router.put("/{category_id}", response_model=category_schema.Category)
def update_category(category_id: int, category: category_schema.CategoryCreate, db: Session = Depends(get_db)):
    return category_service.update_existing_category(db, category_id, category)

