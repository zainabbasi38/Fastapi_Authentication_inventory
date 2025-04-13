from sqlmodel import Field, Relationship
from typing import Optional
from app.models.common import BaseModel
from uuid import UUID
import uuid

class Product(BaseModel, table= True):
    __tablename__ = "products"
    id: Optional[int] = Field(default=None, primary_key=True)
    product_name: str
    description: str
    product_category: Optional[str] = None
    product_price: float
    quantity: int
    status: Optional[str] = Field(default="active")

    user_id: uuid.UUID= Field(default=None, foreign_key="users.id")  # Correct FK reference

    # Relationship to User
    user: Optional["User"] = Relationship(back_populates="products")