from fastapi import Form, Query, Path, Body, File, UploadFile, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import APIRouter
from fastapi import Depends
from enum import Enum
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


http_bearer = HTTPBearer()
example_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@example_router.get("/secure_items/")
async def read_items(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    return {"token": credentials.credentials}


@example_router.get("/secure-endpoint", tags=["secure"], summary="Secure Endpoint", description="This endpoint is secured with OAuth2", response_description="A secure response")
async def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": "This is a secure endpoint"}


@example_router.post("/token", tags=["auth"], summary="Token Endpoint", description="This endpoint provides OAuth2 tokens", response_description="An OAuth2 token")
async def token():
    return {"access_token": "fake-token", "token_type": "bearer"}


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


@example_router.get("/items/{item_id}", tags=['Items'])
async def read_item(
    item_id: int = Path(..., title="The ID of the item to get", ge=1),
    q: Optional[str] = Query(None, max_length=50)
):
    """
    read_item

    Retrieve an item by its ID.

    Parameters:
    - **item_id**: The ID of the item to get. Must be greater than or equal to 1.
    - **q**: An optional query string to filter the results. Maximum length is 50 characters.

    Returns:
    - A dictionary containing the item ID and the query string (if provided).

    Example:
    ```
    {
        "item_id": 1,
        "q": "example"
    }
    ```
    """
    return {"item_id": item_id, "q": q}


@example_router.patch("/broken_items/{item_id}", tags=['Items'])
async def return_error(item_id: int):
    raise HTTPException(detail='test failure', status_code=500)


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
async def read_users(skip: int = 0, limit: int = 200):
    return [User(username=f"user{i}", email=f"user{i}@example.com") for i in range(skip, skip + limit)]

