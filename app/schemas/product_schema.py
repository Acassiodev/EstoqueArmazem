from pydantic import BaseModel

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


    # Em app/schemas/product_schema.py

from pydantic import BaseModel
from .category_schema import Category # <--- 1. IMPORTE O SCHEMA DE CATEGORIA

# ... (Seus schemas ProductBase e ProductCreate continuam os mesmos) ...
class ProductBase(BaseModel):
    sku: str
    name: str
    description: str | None = None

class ProductCreate(ProductBase):
    category_id: int


# 2. MODIFIQUE O SCHEMA DE RESPOSTA 'Product'
class Product(ProductBase):
    id: int
    quantity: int
    # Remova a linha 'category_id: int' se ela existir
    
    category: Category # <--- 3. ADICIONE O CAMPO 'category' COM O TIPO 'Category'

    class Config:
        from_attributes = True



class StockMovementRequest(BaseModel):
    quantity: int