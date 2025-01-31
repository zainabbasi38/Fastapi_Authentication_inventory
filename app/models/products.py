from sqlmodel import Field
from typing import Optional
from app.models.common import BaseModel

class Product(BaseModel, table= True):
    __tablename__= "products"
    product_name : str
    description : str
    product_category : Optional[str]
    product_price : float
    quantity : int
    status : Optional[str]= Field(default="active")

