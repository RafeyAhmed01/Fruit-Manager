from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class FruitCreate(BaseModel):
    name: str
    category_id: int
    price: float
    quantity: int

class FruitResponse(BaseModel):
    id: int
    name: str
    category_id: int
    price: float
    quantity: int
    category: Optional[CategoryResponse] = None

    class Config:
       from_attributes = True