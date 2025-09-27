# Query annotations and validations
from typing import Annotated

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