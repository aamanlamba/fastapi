# Query annotations and validations
from typing import Annotated, Literal

from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# items endpoint with query parameter validation
# str is an optional query parameter with max length of 50
@app.get("/items/")
async def read_items(q: Annotated[str | None, 
                                  Query(title="query parameter",
                                        description="Query string for the items to search in the database that have a good match",
                                        min_length=3, 
                                        max_length=50,
                                        deprecated=True,)] = None,
                                        ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    try:
        if q:
            results.update({"q": q})
    except Exception as e:
        results.update({"error": str(e)})
    return results

# custom validation using pydaantic AfterValidator
from pydantic import AfterValidator
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}


def check_valid_id(id: str):
    if not id.startswith(("isbn-", "imdb-")):
        raise ValueError('Invalid ID format, it must start with "isbn-" or "imdb-"')
    return id

# books endpoint with custom validation
import random
@app.get("/books/")
async def read_book_items(
    id: Annotated[str | None, AfterValidator(check_valid_id)] = None,
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {"id": id, "name": item}

# path annotations and validation
from fastapi import Path
@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get",
                                 ge=1,lt=1000)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# query parameters with Pydantic models
from pydantic import BaseModel, Field, HttpUrl
from fastapi import Query

class FilterParams(BaseModel):
    # do not allow extra fields in the query parameters
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

# endpoint using the FilterParams model for query parameters
# FastAPI will extract the data for each field
# from the query parameters in the request 
# and give you the Pydantic model you defined.
@app.get("/queryitems/")
async def read_query_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

class Image(BaseModel):
    url: HttpUrl
    name: str
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    # optional nested model
    image: Image | None = None

# endpoint with path parameter validation and request body
@app.put("/items/{item_id}")
async def update_item(
    # item_id is a path parameter
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    # item is a request body parameter
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if item:
        # if query parameter q is present, append it to the tags list
        if q:
            item.tags.append(q)
            results.update({"q": q})
        results.update({"item": item})
    return results