from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # "entrada" ou "saida"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    product = relationship("Product", back_populates="movements")