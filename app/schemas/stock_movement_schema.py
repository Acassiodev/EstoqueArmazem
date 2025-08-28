from pydantic import BaseModel
from datetime import datetime

class StockMovement(BaseModel):
    id: int
    quantity: int
    type: str  # "entrada" ou "saida"
    timestamp: datetime
    product_id: int

    class Config:
        from_attributes = True