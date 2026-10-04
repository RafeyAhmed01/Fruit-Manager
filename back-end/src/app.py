from typing import List

from fastapi import FastAPI, HTTPException
from starlette.responses import Response
import json
from fastapi.middleware.cors import CORSMiddleware

from .db import (
    Base,
    create_category,
    create_fruit,
    create_tables,
    delete_category,
    delete_fruit,
    get_all_categories,
    get_all_fruits,
    get_category_by_id,
    get_fruit_by_id,
    update_category,
    update_fruit,
)
from .schemas import CategoryCreate, CategoryResponse, FruitCreate, FruitResponse

app = FastAPI(title="Fruit Management API", description="A simple API to manage fruits using PostgreSQL and SQLAlchemy")

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    """Initialize database tables on startup"""
    create_tables()

# Category CRUD
@app.get("/categories", response_model=List[CategoryResponse])
async def get_categories():
    return get_all_categories()

@app.get("/categories/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int):
    cat = get_category_by_id(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@app.post("/categories", response_model=CategoryResponse)
async def create_category_route(category: CategoryCreate):
    if str(category.name).isdigit():
        raise HTTPException(status_code=400, detail="Category name cannot be just a number. Use a real name.")
    return create_category(category)

@app.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category_route(category_id: int, category: CategoryCreate):
    updated = update_category(category_id, category)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@app.delete("/categories/{category_id}")
async def delete_category_route(category_id: int):
    deleted = delete_category(category_id)
    if isinstance(deleted, dict) and "error" in deleted:
        raise HTTPException(status_code=409, detail=deleted["error"])
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully", "id": category_id}

# Fruit CRUD
@app.get("/fruits", response_model=List[FruitResponse])
async def get_fruits():
    return get_all_fruits()

@app.get("/fruits/{fruit_id}", response_model=FruitResponse)
async def get_fruit(fruit_id: int):
    fruit = get_fruit_by_id(fruit_id)
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return Response(content=json.dumps(FruitResponse.from_orm(fruit).dict(), indent=2, default=str), media_type="application/json")

@app.post("/fruits", response_model=FruitResponse)
async def create_fruit_route(fruit: FruitCreate):
    if str(fruit.name).isdigit():
        raise HTTPException(status_code=400, detail="Fruit name cannot be just a number. Use a real name.")
    return create_fruit(fruit)

@app.put("/fruits/{fruit_id}", response_model=FruitResponse)
async def update_fruit_route(fruit_id: int, fruit: FruitCreate):
    if str(fruit.name).isdigit():
        raise HTTPException(status_code=400, detail="Fruit name cannot be just a number. Use a real name.")
    updated = update_fruit(fruit_id, fruit)
    if not updated:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return updated

@app.delete("/fruits/{fruit_id}")
async def delete_fruit_route(fruit_id: int):
    deleted = delete_fruit(fruit_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Fruit not found")
    return {"message": "Fruit deleted successfully", "id": fruit_id}