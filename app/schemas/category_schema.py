from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de objetos ORM

# Schema base com os campos comuns
class ProductBase(BaseModel):
    sku: str
    name: str
    description: str | None = None

# Schema para a criação de um produto (o que a API recebe)
class ProductCreate(ProductBase):
    category_id: int

# Schema para a exibição de um produto (o que a API retorna)
class Product(ProductBase):
    id: int
    quantity: int
    category_id: int

    class Config:
        from_attributes = True

    
    # Em app/schemas/category_schema.py

from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True # Essencial para ler dados do modelo SQLAlchemy