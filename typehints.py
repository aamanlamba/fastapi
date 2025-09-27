# Type hints: first_name and last_name are strings, function returns a string
def get_full_name(first_name: str, last_name: str) -> str:
    full_name = first_name.title() + " " + last_name.title()
    return full_name
# type hints - validation of type of parameters
def get_name_with_age(name: str, age: int):
    name_with_age = name + " is this old: " + age
    return name_with_age

# type hints - complex data structures like tuples and sets
def process_items(items_t: tuple[int, int, str], items_s: set[bytes]):
    return items_t[2], tuple(items_s)[0]
from typing import Optional


def say_hi(name: str | None = None): # 'name' is now optional
    if name:
        print(f"Hi, {name}!")
    else:
        print("Hi there!")


try:
    print(get_full_name("john", "doe"))  # Output: John Doe
    print(process_items((1, 2, "item"), {b'byte1', b'byte2'}))  # Correct usage
    #print(get_name_with_age("John", 30))  # Correct usage
    say_hi("Alice")  # Output: Hey Alice!
    say_hi(None)  # Output: Hello World
    # print(get_name_with_age("John", "thirty"))  # This will raise a type 
except TypeError as e:
    print(f"Type error: {e}")