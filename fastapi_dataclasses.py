# fastapi_dataclasses.py
from dataclasses import dataclass, field
from typing import List, Union

from fastapi import FastAPI


# A Dataclass as a model used to store and validate data
@dataclass
class Item:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None


app = FastAPI()

# use the dataclass as a request body
# returns a dataclass as a response model
# dataclass is automatically converted to and from JSON by FastAPI as a pydantic model
@app.get("/items/next", response_model=Item)
async def read_next_item():
    return {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be playin' and havin' fun",
        "tags": ["breater"],
    }