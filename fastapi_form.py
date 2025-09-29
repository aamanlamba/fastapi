# fastapi form parameters
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException
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

# createuser receives form fields
@app.post("/createuser/")
async def createuser(userData: Annotated[User, Form()]):
    new_user = None
    if (userData.username) and (userData.password):
        users.append(new_user := User(username=userData.username, 
                                      password=str(hash(userData.password))))
    else:
        raise HTTPException(status_code=400, detail="Username and password required")
    print(new_user)
    return new_user

@app.get("/users/")
async def get_users():
    return users

@app.get("/users/{username}")
async def get_user(username: str):
    for user in users:
        if user.username == username:
            return user
    raise HTTPException(status_code=404, detail="user not found") 

# upload files
from fastapi import File, UploadFile

@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}