# Pydantic example for greater type safety
from pydantic import BaseModel, ValidationError
from datetime import datetime
from typing import Optional, Annotated

class User(BaseModel):  
    id: int
    name: str
    signup_ts: Optional[datetime] = None
    friends: list[int] = []

    def say_hello(self: Annotated[str,"use current object"]) -> str:
        return f"Hello {self.name}"

# Example usage
external_data = {
    "id": "123",
    "name": "John Doe",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)
print(user.say_hello())
# > User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
# > 123