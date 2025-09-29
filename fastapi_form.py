# fastapi form parameters
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
app = FastAPI()

# user model for storing users
# the OAuth2 specification can be used (called "password flow") 
# it is required to send a username and password as form fields.
# The spec requires the fields to be exactly named 
# username and password, and to be sent as form fields, not JSON.
class User(BaseModel):
    username: str = Field(..., example="johndoe")
    password: str = Field(..., example="secret")

users = []
userDB = {}
userCount = 0
# createuser receives form fields
@app.post("/createuser/", response_model=User,
                    status_code=status.HTTP_201_CREATED,
                    tags=["users"])
async def createuser(userData: Annotated[User, Form()]):
    new_user = None
    if (userData.username) and (userData.password):
        users.append(new_user := User(username=userData.username, 
                                      password=str(hash(userData.password))))
        # store the user in a jsonable format
        global userCount
        global userDB
        userDB[userCount] = jsonable_encoder(new_user)
        userCount += 1
        print(userDB)
    else:
        raise HTTPException(status_code=400, detail="Username and password required")
    print(new_user)
    return new_user

@app.get("/users/", response_model=list[User],tags=["users"])
async def get_users():
    return users

@app.get("/users/{username}", response_model=User,tags=["users"])
async def get_user(username: str):
    for user in users:
        if user.username == username:
            return user
    raise HTTPException(status_code=404, detail="user not found") 

# upload files
from fastapi import File, UploadFile

@app.post("/files/",tags=["files"])
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/",tags=["files"])
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

# update items

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]

# update item using PUT and JSON encoding
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

# partial update using PATCH
from fastapi import Body

@app.patch("/items/{item_id}", response_model=Item)
async def patch_item(item_id: str, item: Item = Body(..., example={"name": "New Name", "price": 35.4})):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    # exclude_unset=True means only include fields that were set
    # when creating the item object from the request body
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item_model.model_copy(update=update_data)
    print(updated_item)
    items[item_id] = jsonable_encoder(updated_item)
    return items[item_id]