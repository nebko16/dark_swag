from fastapi import Form, Query, Path, Body, File, UploadFile
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import APIRouter
from enum import Enum


example_router = APIRouter()


class ItemType(str, Enum):
    foo = "foo"
    bar = "bar"
    baz = "baz"


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_offer: bool = False
    tags: List[str] = []
    item_type: ItemType


class User(BaseModel):
    username: str
    email: str = Field(..., example="user@example.com")
    full_name: Optional[str] = None


@example_router.post("/items/", response_model=Item, tags=['Items'])
async def create_item(item: Item):
    return item


@example_router.get("/items/{item_id}", tags=['Items'])
async def read_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=1),
    q: Optional[str] = Query(None, max_length=50)
):
    return {"item_id": item_id, "q": q}


@example_router.put("/items/{item_id}", tags=['Items'])
async def update_item(
    item_id: int,
    item: Item,
    user: User,
    importance: int = Body(..., gt=0),
    q: Optional[str] = None
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

@example_router.post("/things/login/", tags=['Things'])
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}

@example_router.delete("/things/group/{group_id}", tags=['Things'])
async def delete_group(group_id: str):
    return {'success': True}

@example_router.post("/things/files/", tags=['Things'])
async def create_file(
    file: bytes = File(...),
    fileb: UploadFile = File(...),
    token: str = Form(...),
    notes: Optional[str] = Form(None)
):
    return {
        "file_size": len(file),
        "token": token,
        "notes": notes,
        "fileb_content_type": fileb.content_type
    }


@example_router.get("/things/users/", response_model=List[User], tags=['Things'])
async def read_users(skip: int = 0, limit: int = 10):
    return [User(username=f"user{i}", email=f"user{i}@example.com") for i in range(skip, skip + limit)]

