# fastapi_param_dependency.py
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()

# a Callable class as a dependency
class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    # when called as a dependency, it will check if the fixed content is in the query parameter
    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False

# create an instance of the class with the fixed content to check
checker = FixedContentQueryChecker("bar")

# use the instance as a dependency in the endpoint
@app.get("/query-checker/")
async def read_query_check(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {"fixed_content_in_query": fixed_content_included}